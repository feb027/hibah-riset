"""Core AI Analytics Pipeline Orchestrator.

Menghubungkan Detektor YOLO26, Tracker Deep-OC-SORT, dan Logika PeopleCounter.
Terisolasi penuh dari framework web (Pure Python Domain Logic).
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import numpy as np

# Ultralytics requirements check bypass untuk lingkungan Windows DirectML
try:
    import ultralytics.utils.checks
    import ultralytics.nn.autobackend
    import ultralytics.engine.predictor
    _orig_check = ultralytics.utils.checks.check_requirements
    def _custom_check(reqs, *args, **kwargs):
        if "onnxruntime" in str(reqs):
            return True
        return _orig_check(reqs, *args, **kwargs)
    ultralytics.utils.checks.check_requirements = _custom_check
    ultralytics.nn.autobackend.check_requirements = _custom_check
    ultralytics.engine.predictor.check_requirements = _custom_check
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from core.counting.counter import PeopleCounter  # noqa: E402
from core.counting.detector import PolygonDetector  # noqa: E402
from core.counting.models import Line, Point, Polygon  # noqa: E402
from src.deepocsort import DeepOCSortTracker  # noqa: E402
from src.lighttrack.phase4_onnx import TbssAppearanceOnnx  # noqa: E402
from src.web.core.telemetry import TelemetryHub  # noqa: E402
from src.web.schemas.config import LineConfigDTO, PointDTO, RoiConfigDTO  # noqa: E402
from src.web.schemas.telemetry import TelemetryPayload, TrackBoxDTO  # noqa: E402

OCSORT_ROOT = os.path.join(str(ROOT), "external", "OC_SORT")
sys.path.insert(0, OCSORT_ROOT)
from trackers.ocsort_tracker.ocsort import OCSort  # noqa: E402


def _id_to_color_hex(track_id: int) -> str:
    """Golden Ratio Hue Generator untuk warna ID yang konsisten dan kontras tinggi."""
    hue = (track_id * 61) % 180
    bgr = cv2.cvtColor(np.uint8([[[hue, 220, 240]]]), cv2.COLOR_HSV2BGR)[0][0]
    return f"#{int(bgr[2]):02x}{int(bgr[1]):02x}{int(bgr[0]):02x}"


def _id_to_bgr(track_id: int) -> Tuple[int, int, int]:
    hue = (track_id * 61) % 180
    bgr = cv2.cvtColor(np.uint8([[[hue, 220, 240]]]), cv2.COLOR_HSV2BGR)[0][0]
    return (int(bgr[0]), int(bgr[1]), int(bgr[2]))


class EnginePipeline:
    """Orkestrator inferensi AI yang mengelola siklus Deteksi -> Tracking -> Counting."""

    def __init__(
        self,
        weights_path: Optional[str] = None,
        tracker_name: str = "deepocsort",
        cooldown: int = 30,
        conf_thresh: float = 0.3,
    ):
        self.weights_path = weights_path or str(ROOT / "data" / "s2" / "weights" / "best.onnx")
        self.tracker_name = tracker_name
        self.cooldown = cooldown
        self.conf_thresh = conf_thresh

        # Inisialisasi Detektor
        from ultralytics import YOLO
        print(f"[EnginePipeline] Memuat detektor YOLO: {self.weights_path}")
        self.model = YOLO(self.weights_path)

        # Inisialisasi Tracker
        self._init_tracker()

        # Inisialisasi RoI dan Garis Virtual Default (1/3 Lebar Frame)
        self.line_dto = LineConfigDTO(
            start=PointDTO(x=0.33, y=0.0),
            end=PointDTO(x=0.33, y=1.0),
            orientation="v",
        )
        self.roi_dto = RoiConfigDTO(
            enabled=False,
            points=[
                PointDTO(x=0.05, y=0.1),
                PointDTO(x=0.90, y=0.1),
                PointDTO(x=0.90, y=0.95),
                PointDTO(x=0.05, y=0.95),
            ],
        )

        self._roi_polygon: Optional[Polygon] = None
        self._build_counter()

        # Telemetry Hub
        self.telemetry_hub = TelemetryHub()
        self.telemetry_hub.set_source_and_model("Source Stream", f"YOLO26-S + {tracker_name.upper()}")

    def _init_tracker(self) -> None:
        if self.tracker_name == "deepocsort":
            onnx_dir = ROOT / "out" / "onnx"
            appearance = TbssAppearanceOnnx(str(onnx_dir))
            self.tracker = DeepOCSortTracker(
                det_thresh=self.conf_thresh, max_age=30, min_hits=3,
                iou_threshold=0.3, delta_t=3, inertia=0.2,
                w_association_emb=0.5, alpha_fixed_emb=0.9,
                appearance=appearance,
            )
        elif self.tracker_name == "ocsort":
            self.tracker = OCSort(
                det_thresh=self.conf_thresh, max_age=30, min_hits=3,
                iou_threshold=0.3, delta_t=3, asso_func="iou", inertia=0.2,
            )
        else:
            self.tracker_name = "ocsort"
            self.tracker = OCSort(det_thresh=self.conf_thresh, max_age=30, min_hits=3)

    def _build_counter(self) -> None:
        # Konversi fraksi ke garis internal (dinormalisasi atau dipetakan saat frame masuk)
        # VirtualLine internal default
        vl = Line(
            start=Point(self.line_dto.start.x, self.line_dto.start.y),
            end=Point(self.line_dto.end.x, self.line_dto.end.y),
        )
        roi_poly = None
        if self.roi_dto.enabled and len(self.roi_dto.points) >= 3:
            roi_poly = Polygon(points=[Point(p.x, p.y) for p in self.roi_dto.points])
        self._roi_polygon = roi_poly
        self.counter = PeopleCounter(virtual_line=vl, cooldown_threshold=self.cooldown, roi=roi_poly)

    def set_line(self, start: PointDTO, end: PointDTO, orientation: str = "custom") -> None:
        """Pembaruan koordinat garis virtual secara dinamis."""
        self.line_dto = LineConfigDTO(start=start, end=end, orientation=orientation)
        # Pertahankan data hitungan saat garis digeser
        saved_in = self.counter.count_in
        saved_out = self.counter.count_out
        saved_tracks = self.counter._tracks
        self._build_counter()
        self.counter.count_in = saved_in
        self.counter.count_out = saved_out
        self.counter._tracks = saved_tracks
        print(f"[EnginePipeline] Garis diperbarui: ({start.x:.2f},{start.y:.2f}) -> ({end.x:.2f},{end.y:.2f})")

    def set_roi(self, points: List[PointDTO], enabled: bool) -> None:
        """Pembaruan konfigurasi zona RoI secara dinamis."""
        self.roi_dto = RoiConfigDTO(enabled=enabled, points=points)
        saved_in = self.counter.count_in
        saved_out = self.counter.count_out
        saved_tracks = self.counter._tracks
        self._build_counter()
        self.counter.count_in = saved_in
        self.counter.count_out = saved_out
        self.counter._tracks = saved_tracks
        print(f"[EnginePipeline] RoI diperbarui: enabled={enabled}, titik={len(points)}")

    def flip_direction(self) -> None:
        """Membalik arah garis virtual (menukar posisi Titik A dan Titik B)."""
        new_start = self.line_dto.end
        new_end = self.line_dto.start
        self.set_line(new_start, new_end, self.line_dto.orientation)

    def reset_counts(self) -> None:
        """Reset seluruh akumulator hitungan ke 0."""
        self.counter.count_in = 0
        self.counter.count_out = 0
        self.counter._tracks = {}
        self.telemetry_hub.reset_history()
        print("[EnginePipeline] Hitungan di-reset ke 0.")

    def process_frame(self, frame_bgr: np.ndarray) -> Tuple[np.ndarray, TelemetryPayload]:
        """Eksekusi inferensi end-to-end pada 1 frame video."""
        t0 = time.perf_counter()
        h, w = frame_bgr.shape[:2]

        # 1. Pastikan koordinat garis dan RoI dipetakan ke ukuran frame aktual
        # Jika nilai DTO adalah fraksi (<= 1.0), skalakan ke piksel frame
        p1_px = Point(
            int(self.line_dto.start.x * w) if self.line_dto.start.x <= 1.0 else int(self.line_dto.start.x),
            int(self.line_dto.start.y * h) if self.line_dto.start.y <= 1.0 else int(self.line_dto.start.y),
        )
        p2_px = Point(
            int(self.line_dto.end.x * w) if self.line_dto.end.x <= 1.0 else int(self.line_dto.end.x),
            int(self.line_dto.end.y * h) if self.line_dto.end.y <= 1.0 else int(self.line_dto.end.y),
        )
        self.counter.virtual_line = Line(start=p1_px, end=p2_px)

        roi_px_polygon = None
        if self.roi_dto.enabled and len(self.roi_dto.points) >= 3:
            roi_px_points = [
                Point(
                    int(p.x * w) if p.x <= 1.0 else int(p.x),
                    int(p.y * h) if p.y <= 1.0 else int(p.y),
                )
                for p in self.roi_dto.points
            ]
            roi_px_polygon = Polygon(points=roi_px_points)
            self.counter.roi = roi_px_polygon
        else:
            self.counter.roi = None

        # 2. Deteksi Objek YOLO26
        results = self.model.predict(frame_bgr, imgsz=640, conf=self.conf_thresh, verbose=False)[0]
        boxes = results.boxes
        dets_xyxy = []
        scores = []
        if boxes is not None and len(boxes) > 0:
            xyxy_arr = boxes.xyxy.cpu().numpy()
            conf_arr = boxes.conf.cpu().numpy()
            cls_arr = boxes.cls.cpu().numpy()
            for b_idx in range(len(xyxy_arr)):
                if int(cls_arr[b_idx]) == 0:  # person class
                    dets_xyxy.append(xyxy_arr[b_idx])
                    scores.append(float(conf_arr[b_idx]))
        dets_xyxy = np.array(dets_xyxy, dtype=np.float64).reshape(-1, 4)
        scores = np.array(scores, dtype=np.float64).reshape(-1)

        # 3. Asosiasi Tracking
        if self.tracker_name == "deepocsort":
            online = self.tracker.update(dets_xyxy, scores, frame_bgr=frame_bgr)
            raw_tracks = []
            for (bx, by, bw, bh), tid in online:
                raw_tracks.append((bx, by, bx + bw, by + bh, int(tid)))
        else:
            cates = np.zeros(dets_xyxy.shape[0])
            online = self.tracker.update_public(dets_xyxy, cates, scores)
            raw_tracks = []
            for trk in online:
                raw_tracks.append((trk[0], trk[1], trk[2], trk[3], int(trk[4])))

        # 4. Filter RoI & Evaluasi PeopleCounter
        active_tracks: List[TrackBoxDTO] = []
        live_occupancy = 0
        display = frame_bgr.copy()

        for x1, y1, x2, y2, tid in raw_tracks:
            cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
            is_in_roi = True
            if roi_px_polygon is not None:
                is_in_roi = PolygonDetector.is_inside(roi_px_polygon, Point(cx, cy))

            color_bgr = _id_to_bgr(tid)
            color_hex = _id_to_color_hex(tid)

            if is_in_roi:
                live_occupancy += 1
                self.counter.update(tid, Point(cx, cy))
                # Gambar kotak aktif
                cv2.rectangle(display, (int(x1), int(y1)), (int(x2), int(y2)), color_bgr, 2)
                cv2.circle(display, (int(cx), int(cy)), 3, color_bgr, -1)
                cv2.putText(display, f"ID {tid}", (int(x1), max(int(y1) - 6, 14)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, color_bgr, 1, cv2.LINE_AA)
            else:
                # Objek di luar RoI digambar abu-abu redup
                cv2.rectangle(display, (int(x1), int(y1)), (int(x2), int(y2)), (70, 70, 70), 1)

            active_tracks.append(
                TrackBoxDTO(
                    track_id=tid,
                    x1=round(x1 / w, 4),
                    y1=round(y1 / h, 4),
                    x2=round(x2 / w, 4),
                    y2=round(y2 / h, 4),
                    cx=round(cx / w, 4),
                    cy=round(cy / h, 4),
                    is_in_roi=is_in_roi,
                    color_hex=color_hex,
                )
            )

        # Hitung latensi & perbarui telemetri
        dt_ms = (time.perf_counter() - t0) * 1000.0
        self.telemetry_hub.update_performance(dt_ms)
        self.telemetry_hub.update_counts(
            total=self.counter.count_in + self.counter.count_out,
            count_in=self.counter.count_in,
            count_out=self.counter.count_out,
            occupancy=live_occupancy,
        )

        telemetry_payload = self.telemetry_hub.build_payload(
            line=self.line_dto,
            roi=self.roi_dto,
            tracks=active_tracks,
        )

        return display, telemetry_payload
