#!/usr/bin/env python3
"""Demo realtime: YOLO26 (ONNX) + OC-SORT + counting garis virtual.

Pipeline Skenario A (deteksi YOLO26 fine-tune CrowdHuman) + Skenario B
(tracking OC-SORT) + counting garis virtual (IN/OUT) dengan HUD FPS.

Sumber video: webcam (--source 0) ATAU file video (--source path.mp4).
Bobot: default data/s2/weights/best.onnx (ONNX Runtime, CPU). Bisa juga .pt
(kalau torch+CUDA tersedia, ultralytics otomatis pakai GPU).

Contoh:
    python scripts/s2/realtime_demo.py --source 0
    python scripts/s2/realtime_demo.py --source video.mp4 --line 0.33 --save out.mp4
    python scripts/s2/realtime_demo.py --source video.mp4 --tracker lighttrack \
        --ckpt out/phase3_fold1_v2/best.pt --save out_lighttrack.mp4

Tombol: ESC keluar, SPACE pause, C reset hitungan.

Konvensi arah: kiri->kanan = IN, kanan->kiri = OUT (sama dengan eksperimen Skenario C).
py3.8-compatible (bisa jalan di PC kampus).
"""
import argparse
import os
import sys
import time

import cv2
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from core.counting.counter import PeopleCounter          # noqa: E402
from core.counting.models import Line, Point             # noqa: E402

OCSORT_ROOT = os.path.join(ROOT, "external", "OC_SORT")
sys.path.insert(0, OCSORT_ROOT)
from trackers.ocsort_tracker.ocsort import OCSort        # noqa: E402


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--source", required=True,
                   help="webcam index (mis. 0) atau path file video (mis. video.mp4)")
    p.add_argument("--weights", default=os.path.join(ROOT, "data", "s2", "weights", "best.onnx"),
                   help="bobot YOLO26 (.onnx untuk ONNX Runtime CPU; .pt untuk torch/GPU)")
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--conf", type=float, default=0.3)
    p.add_argument("--cls", type=int, default=0, help="class yang dilacak (0 = person)")
    p.add_argument("--line", type=float, default=0.33,
                   help="posisi garis VERTIKAL sbg fraksi lebar frame (0..1); -1 = tanpa counting")
    p.add_argument("--line-y", type=float, default=-1,
                   help="posisi garis HORIZONTAL sbg fraksi tinggi frame (0..1); dipakai bila >= 0 "
                        "(menggantikan --line). Cocok untuk video dengan gerak atas->bawah")
    p.add_argument("--cooldown", type=int, default=30, help="frame cooldown anti double-count")
    # parameter tracker — identik dengan run Skenario B
    p.add_argument("--track-thresh", type=float, default=0.3)
    p.add_argument("--max-age", type=int, default=30)
    p.add_argument("--min-hits", type=int, default=3)
    p.add_argument("--iou-thresh", type=float, default=0.3)
    p.add_argument("--delta-t", type=int, default=3)
    p.add_argument("--asso", default="iou", choices=["iou", "giou", "ciou", "diou"])
    p.add_argument("--inertia", type=float, default=0.2)
    p.add_argument("--max-w", type=int, default=960, help="lebar tampilan maksimum")
    p.add_argument("--save", default=None, help="simpan hasil ke file mp4 (opsional)")
    p.add_argument("--no-show", action="store_true",
                   help="headless: tanpa window (buat mesin tanpa display spt JupyterHub); "
                        "video berjalan sampai habis, tombol keyboard nonaktif")
    p.add_argument("--tracker", default="ocsort", choices=["ocsort", "lighttrack"],
                   help="ocsort (default) atau lighttrack (usulan kita: LAE+TBSS+OCM)")
    p.add_argument("--ckpt", default=None,
                   help="wajib saat --tracker lighttrack: ckpt LAE+TBSS "
                        "(mis. out/phase3_fold1_v2/best.pt)")
    p.add_argument("--onnx-dir", default=None,
                   help="jalan LightTrack tanpa torch: folder berisi lae.onnx + tbss.onnx "
                        "(hasil scripts/s2/export_lighttrack_onnx.py). Untuk PC tanpa "
                        "torch-GPU (mis. Windows + RX6600 via DirectML). ")
    p.add_argument("--appearance-w", type=float, default=0.5)
    p.add_argument("--score-min", type=float, default=0.3)
    p.add_argument("--emit-age", type=int, default=5)
    p.add_argument("--ema-alpha", type=float, default=0.9,
                   help="EMA embedding tracklet (LightTrack); default 0.9 = sama dgn eval final")
    p.add_argument("--cmoh-k", type=int, default=10)
    return p.parse_args()


def box_color(track_id):
    hue = (track_id * 61) % 180
    bgr = cv2.cvtColor(np.uint8([[[hue, 255, 255]]]), cv2.COLOR_HSV2BGR)[0][0]
    return (int(bgr[0]), int(bgr[1]), int(bgr[2]))


def main():
    args = parse_args()
    from ultralytics import YOLO

    if not os.path.exists(args.weights):
        sys.exit("Bobot tidak ditemukan: %s (export ONNX: yolo export model=data/s2/weights/best.pt format=onnx)" % args.weights)
    if not os.path.isdir(OCSORT_ROOT):
        sys.exit("Repo OC_SORT tidak ditemukan di %s" % OCSORT_ROOT)

    print("Memuat model:", args.weights)
    model = YOLO(args.weights)

    source = int(args.source) if str(args.source).isdigit() else args.source
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        sys.exit("Gagal membuka sumber video: %s" % args.source)

    ok, first_frame = cap.read()
    if not ok:
        sys.exit("Gagal membaca frame pertama dari sumber: %s" % args.source)
    frame_h, frame_w = first_frame.shape[:2]

    # ONNX: ultralytics default bikin session CPU. Kalau DirectML tersedia,
    # pemanasan sekali (membangun predictor), lalu TUKAR session-nya ke DML
    # supaya deteksi jalan di GPU (RX6600) bukan CPU.
    if str(args.weights).lower().endswith(".onnx"):
        import onnxruntime as ort
        if "DmlExecutionProvider" in ort.get_available_providers():
            print("DirectML tersedia — mengalihkan deteksi ke GPU (DML) ...")
            # source=array: pemanasan, hasilnya tak dipakai; predictor jadi ada
            model.predict(source=first_frame, verbose=False)
            sess = ort.InferenceSession(
                str(args.weights),
                providers=["DmlExecutionProvider", "CPUExecutionProvider"])
            model.predictor.model.session = sess
            print("Deteksi ONNX sekarang memakai DmlExecutionProvider.")
        else:
            print("DirectML tidak tersedia — deteksi ONNX di CPU.")

    if args.tracker == "lighttrack":
        if args.onnx_dir:
            sys.path.insert(0, ROOT)
            from src.lighttrack.tracker import LightTrackTracker        # noqa: E402
            from src.lighttrack.phase4_onnx import TbssAppearanceOnnx   # noqa: E402
            appearance = TbssAppearanceOnnx(args.onnx_dir)
        else:
            if not args.ckpt:
                sys.exit("--tracker lighttrack butuh --ckpt (mis. out/phase3_fold1_v2/best.pt) "
                         "atau --onnx-dir (folder lae.onnx + tbss.onnx)")
            if not os.path.exists(args.ckpt):
                sys.exit("CKPT tidak ditemukan: %s" % args.ckpt)
            sys.path.insert(0, ROOT)
            from src.lighttrack.tracker import LightTrackTracker        # noqa: E402
            from src.lighttrack.phase4 import TbssAppearance            # noqa: E402
            appearance = TbssAppearance(args.ckpt)
        tracker = LightTrackTracker(min_conf=args.track_thresh, iou_thresh=args.iou_thresh,
                                    min_hits=args.min_hits, max_age=args.max_age,
                                    ema_alpha=args.ema_alpha, emit_age=args.emit_age,
                                    appearance=appearance,
                                    appearance_w=args.appearance_w,
                                    score_min=args.score_min, cmoh_k=args.cmoh_k)
    else:
        tracker = OCSort(
            args.track_thresh,
            max_age=args.max_age,
            min_hits=args.min_hits,
            iou_threshold=args.iou_thresh,
            delta_t=args.delta_t,
            asso_func=args.asso,
            inertia=args.inertia,
        )

    counter = None
    line_pos = None
    line_ori = "v"
    if args.line_y >= 0:
        vy = int(frame_h * args.line_y)
        counter = PeopleCounter(Line(Point(0, vy), Point(frame_w, vy)),
                                cooldown_threshold=args.cooldown)
        line_pos = args.line_y
        line_ori = "h"
    elif args.line >= 0:
        vx = int(frame_w * args.line)
        counter = PeopleCounter(Line(Point(vx, 0), Point(vx, frame_h)),
                                cooldown_threshold=args.cooldown)
        line_pos = args.line
        line_ori = "v"

    writer = None
    if args.save:
        writer = cv2.VideoWriter(args.save, cv2.VideoWriter_fourcc(*"mp4v"), 30,
                                 (min(frame_w, args.max_w), int(frame_h * min(1.0, args.max_w / float(frame_w)))))

    fps = 0.0
    paused = False
    frame = first_frame
    print("Jalan! ESC = keluar, SPACE = pause, C = reset hitungan.")
    print("(counting %s, garis %s=%.2f)" % ("AKTIF" if counter else "nonaktif",
                                            line_ori, line_pos if line_pos is not None else -1))

    while True:
        if not paused:
            t0 = time.perf_counter()

            results = model.predict(frame, imgsz=args.imgsz, conf=args.conf, verbose=False)
            boxes = results[0].boxes
            dets_xyxy = []
            scores = []
            if boxes is not None and len(boxes) > 0:
                xyxy = boxes.xyxy.cpu().numpy()
                conf = boxes.conf.cpu().numpy()
                cls = boxes.cls.cpu().numpy()
                for i in range(len(xyxy)):
                    if args.cls is None or int(cls[i]) == args.cls:
                        dets_xyxy.append(xyxy[i])
                        scores.append(float(conf[i]))
            dets_xyxy = np.array(dets_xyxy, dtype=np.float64).reshape(-1, 4)
            scores = np.array(scores, dtype=np.float64).reshape(-1)

            cates = np.zeros(dets_xyxy.shape[0])
            if args.tracker == "lighttrack":
                # LightTrack: butuh tlwh + frame asli untuk embedding LAE
                tlwh = np.zeros_like(dets_xyxy)
                tlwh[:, 0] = dets_xyxy[:, 0]
                tlwh[:, 1] = dets_xyxy[:, 1]
                tlwh[:, 2] = dets_xyxy[:, 2] - dets_xyxy[:, 0]
                tlwh[:, 3] = dets_xyxy[:, 3] - dets_xyxy[:, 1]
                online = [(b, i) for b, i in tracker.update(tlwh, scores, frame_bgr=frame)]
            else:
                online = tracker.update_public(dets_xyxy, cates, scores)

            # overlay
            display = frame.copy()
            h, w = display.shape[:2]
            active = {}
            for trk in online:
                if args.tracker == "lighttrack":
                    bx, by, bw, bh = trk[0]
                    x1, y1, x2, y2, tid = bx, by, bx + bw, by + bh, int(trk[1])
                else:
                    x1, y1, x2, y2, tid = trk[0], trk[1], trk[2], trk[3], int(trk[4])
                color = box_color(tid)
                cv2.rectangle(display, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                cv2.putText(display, "ID %d" % tid, (int(x1), max(int(y1) - 6, 14)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
                active[tid] = ((x1 + x2) / 2.0, (y1 + y2) / 2.0)

            if counter is not None:
                if line_ori == "h":
                    vy = int(h * line_pos)
                    cv2.line(display, (0, vy), (w, vy), (255, 255, 0), 2)
                    cv2.putText(display, "IN (atas->bawah)", (8, max(vy - 8, 14)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
                else:
                    vx = int(w * line_pos)
                    cv2.line(display, (vx, 0), (vx, h), (255, 255, 0), 2)
                    cv2.putText(display, "IN (kiri->kanan)", (vx + 8, 24),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
                for tid, (cx, cy) in active.items():
                    counter.update(tid, Point(cx, cy))
                total = counter.count_in + counter.count_out
                cv2.putText(display, "TOTAL %d  IN %d  OUT %d" % (total, counter.count_in, counter.count_out),
                            (10, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(display, "TRACK %d" % len(active), (10, 34),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)

            dt = time.perf_counter() - t0
            fps = 0.9 * fps + 0.1 * (1.0 / max(dt, 1e-6))
            cv2.putText(display, "FPS %.1f | deteksi %.1f ms" % (fps, dt * 1000),
                        (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

            if display.shape[1] > args.max_w:
                scale = args.max_w / float(display.shape[1])
                display = cv2.resize(display, (args.max_w, int(display.shape[0] * scale)))
            if not args.no_show:
                cv2.imshow("YOLO26 + OC-SORT (realtime)", display)
            if writer is not None:
                writer.write(display)

            # baca frame berikutnya (setelah proses selesai)
            ok, frame = cap.read()
            if not ok:
                print("Sumber selesai/putus.")
                break

        if args.no_show:
            continue
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == 32:  # SPACE
            paused = not paused
        elif key in (ord("c"), ord("C")) and counter is not None:
            counter.count_in = counter.count_out = 0
            counter._tracks = {}

    cap.release()
    if writer is not None:
        writer.release()
    if not args.no_show:
        cv2.destroyAllWindows()
    if counter is not None:
        print("Selesai. TOTAL=%d IN=%d OUT=%d (FPS rata-rata %.1f)"
              % (counter.count_in + counter.count_out, counter.count_in,
                 counter.count_out, fps))


if __name__ == "__main__":
    main()
