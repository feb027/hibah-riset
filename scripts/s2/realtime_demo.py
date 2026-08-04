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
            online = tracker.update_public(dets_xyxy, cates, scores)

            # overlay
            display = frame.copy()
            h, w = display.shape[:2]
            active = {}
            for trk in online:
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
            cv2.imshow("YOLO26 + OC-SORT (realtime)", display)
            if writer is not None:
                writer.write(display)

            # baca frame berikutnya (setelah proses selesai)
            ok, frame = cap.read()
            if not ok:
                print("Sumber selesai/putus.")
                break

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
    cv2.destroyAllWindows()
    if counter is not None:
        print("Selesai. TOTAL=%d IN=%d OUT=%d (FPS rata-rata %.1f)"
              % (counter.count_in + counter.count_out, counter.count_in,
                 counter.count_out, fps))


if __name__ == "__main__":
    main()
