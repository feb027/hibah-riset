#!/usr/bin/env python3
"""Demo realtime DiffMOT (CVPR 2024) — headless, save mp4.

Pipeline: YOLO26 fine-tune (deteksi) + DiffMOT (D2MP motion predictor +
ReID SBS/osnet + association) + HUD FPS. Dirancang untuk PC kampus
(RTX 4090, akses via Jupyter/terminal, TANPA display) — hasil video
disimpan ke mp4. Juga bisa --show di PC rumah kalau ada GPU + display.

Deteksi dari YOLO26 fine-tune (Skenario A), seperti skenario B. Tracker =
diffmottracker dari repo Kroery/DiffMOT dengan patch
scripts/s2/patch_diffmot_eval.py (harus sudah di-patch di kampus —
run_skenario_b_diffmot.py ensure melakukannya otomatis).

Perbedaan dengan eval: source asli meng-komentari `img` (pakai cache
embedding pkl). Demo ini TIDAK punya cache → img wajib dikirim, embedding
ReID dihitung live per frame. Ini jalur yang benar untuk realtime.

Contoh:
  python scripts/s2/realtime_demo_diffmot.py --source video.mp4 --save demo_diffmot.mp4
  python scripts/s2/realtime_demo_diffmot.py --source 0 --dataset dancetrack --save cam.mp4 --show
  python scripts/s2/realtime_demo_diffmot.py --check   # verifikasi path+import, tanpa run

Arg:
  --source       path video ATAU index webcam (default 0)
  --dataset      mot | dancetrack  (default mot; pilih ReID + ckpt D2MP)
  --ckpt         path ckpt D2MP; default <diffmot-root>/experiments/
                 diffmot_{mot,dance}/..._epoch800.pt
  --weights      YOLO26 .pt (GPU); default data/s2/weights/best.pt
  --imgsz / --conf / --cls  parameter deteksi (default 640 / 0.3 / 0=person)
  --save         path mp4 output (WAJIB kalau headless; default
                 experiments/s2_tracker/demo/diffmot_realtime.mp4)
  --show         tampilkan window (butuh display)
  --max-w        lebar maksimum output (default 960)
  --diffmot-root repo Kroery/DiffMOT (default external/diffmot)
"""
from __future__ import annotations

import argparse
import os
import sys
import time

import cv2
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--source", default="0", help="path video atau index webcam (default 0)")
    p.add_argument("--dataset", default="mot", choices=["mot", "dancetrack"])
    p.add_argument("--ckpt", default=None, help="ckpt D2MP (.pt); default auto dari dataset")
    p.add_argument("--weights", default=os.path.join(ROOT, "data", "s2", "weights", "best.pt"))
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--conf", type=float, default=0.3)
    p.add_argument("--cls", type=int, default=0, help="class yang dilacak (0 = person)")
    p.add_argument("--save", default=None, help="mp4 output; default experiments/s2_tracker/demo/diffmot_realtime.mp4")
    p.add_argument("--show", action="store_true", help="tampilkan window (butuh display)")
    p.add_argument("--max-w", type=int, default=960)
    p.add_argument("--diffmot-root", default=os.path.join(ROOT, "external", "diffmot"))
    p.add_argument("--check", action="store_true", help="verifikasi path/import/CUDA lalu exit")
    return p.parse_args()


def auto_ckpt(a: argparse.Namespace) -> str:
    name = "mot" if a.dataset == "mot" else "dancetrack"
    exp = "diffmot_mot" if a.dataset == "mot" else "diffmot_dance"
    return os.path.join(a.diffmot_root, "experiments", exp, f"{name}_epoch800.pt")


def box_color(track_id):
    hue = (track_id * 61) % 180
    bgr = cv2.cvtColor(np.uint8([[[hue, 255, 255]]]), cv2.COLOR_HSV2BGR)[0][0]
    return (int(bgr[0]), int(bgr[1]), int(bgr[2]))


def check(a: argparse.Namespace) -> int:
    errs = []
    for label, path in [("YOLO weights", a.weights), ("ckpt D2MP", a.ckpt),
                        ("diffmot root", a.diffmot_root)]:
        if not os.path.exists(path):
            errs.append(f"{label} tidak ada: {path}")
    if not errs:
        sys.path.insert(0, a.diffmot_root)
        try:
            from models.autoencoder import D2MP                      # noqa: F401
            from models.condition_embedding import History_motion_embedding  # noqa: F401
            from tracker.DiffMOTtracker import diffmottracker        # noqa: F401
            print("import DiffMOT: OK")
        except Exception as e:
            errs.append(f"import DiffMOT gagal: {e!r}")
        try:
            import torch
            print(f"python : {sys.executable}")
            print(f"torch  : {torch.__version__} | cuda={torch.cuda.is_available()}")
            if not torch.cuda.is_available():
                errs.append("CUDA tidak aktif — DiffMOT butuh GPU")
        except Exception as e:
            errs.append(f"torch gagal: {e!r}")
    if errs:
        print("\n".join("!! " + e for e in errs))
        return 1
    print("OK — siap run.")
    return 0


def main() -> int:
    a = parse_args()
    a.ckpt = a.ckpt or auto_ckpt(a)
    if a.check:
        return check(a)
    if a.save is None:
        a.save = os.path.join(ROOT, "experiments", "s2_tracker", "demo", "diffmot_realtime.mp4")

    if not os.path.exists(a.diffmot_root):
        sys.exit("diffmot root tidak ada: %s" % a.diffmot_root)
    if not os.path.exists(a.ckpt):
        sys.exit("ckpt D2MP tidak ada: %s" % a.ckpt)
    if not os.path.exists(a.weights):
        sys.exit("weights YOLO tidak ada: %s" % a.weights)

    # Path relatif ReID ("external/weights/...") di-resolve dari cwd diffmot.
    os.chdir(a.diffmot_root)
    a.save = os.path.abspath(a.save)
    os.makedirs(os.path.dirname(a.save), exist_ok=True)

    import torch
    from easydict import EasyDict
    sys.path.insert(0, a.diffmot_root)
    from models.autoencoder import D2MP
    from models.condition_embedding import History_motion_embedding
    from tracker.DiffMOTtracker import diffmottracker

    assert torch.cuda.is_available(), "DiffMOT butuh GPU (CUDA tidak aktif)"
    torch.backends.cudnn.benchmark = True
    print("GPU:", torch.cuda.get_device_name(0))

    # --- D2MP motion predictor (config sama dgn make_config di run_skenario_b_diffmot) ---
    config = EasyDict(dict(
        dataset=a.dataset,
        diffnet="HMINet", encoder_dim=256, tf_layer=3, eps=0.001,
        high_thres=0.4 if a.dataset == "mot" else 0.6,
        low_thres=0.1 if a.dataset == "mot" else 0.4,
        w_assoc_emb=2.2, aw_param=1.7,
        reid_dir=os.path.join(ROOT, "data", "s2", "embeddings", "demo"),
    ))
    print("Load ckpt D2MP:", a.ckpt)
    ckpt = torch.load(a.ckpt, map_location="cpu")
    model = D2MP(config, encoder=History_motion_embedding()).cuda().eval()
    model.load_state_dict({k.replace("module.", ""): v for k, v in ckpt["ddpm"].items()})
    print("D2MP OK. Load YOLO:", a.weights)
    from ultralytics import YOLO
    detector = YOLO(a.weights)

    # --- sumber video ---
    source = int(a.source) if str(a.source).isdigit() else a.source
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        sys.exit("Gagal membuka sumber: %s" % a.source)
    ok, frame = cap.read()
    if not ok:
        sys.exit("Gagal membaca frame pertama dari: %s" % a.source)
    frame_h, frame_w = frame.shape[:2]
    src_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    writer = cv2.VideoWriter(a.save, cv2.VideoWriter_fourcc(*"mp4v"), src_fps,
                             (min(frame_w, a.max_w), int(frame_h * min(1.0, a.max_w / float(frame_w)))))
    print("Output:", a.save, "| frame %dx%d @ %.0f fps" % (frame_w, frame_h, src_fps))

    tracker = diffmottracker(config)
    fps = 0.0
    frame_id = 1
    print("Jalan! (headless — hasil di mp4; Ctrl+C untuk stop)")

    try:
        while True:
            t0 = time.perf_counter()
            results = detector.predict(frame, imgsz=a.imgsz, conf=a.conf, verbose=False)
            boxes = results[0].boxes
            dets = []  # [x1, y1, w, h, score] (TLWH) — format yang diterima diffmottracker.update
            if boxes is not None and len(boxes) > 0:
                xyxy = boxes.xyxy.cpu().numpy()
                confs = boxes.conf.cpu().numpy()
                clss = boxes.cls.cpu().numpy()
                for i in range(len(xyxy)):
                    if int(clss[i]) == a.cls:
                        x1, y1, x2, y2 = xyxy[i]
                        dets.append([x1, y1, x2 - x1, y2 - y1, float(confs[i])])
            dets = np.asarray(dets, dtype=np.float32).reshape(-1, 5)

            tag = "demo:%d" % frame_id
            online = tracker.update(dets, model, frame_id, frame_w, frame_h, tag, frame)

            display = frame.copy()
            for t in online:
                x1, y1, w, h = t.tlwh
                color = box_color(t.track_id)
                cv2.rectangle(display, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), color, 2)
                cv2.putText(display, "ID %d" % t.track_id, (int(x1), max(int(y1) - 6, 14)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
            dt = time.perf_counter() - t0
            fps = 0.9 * fps + 0.1 * (1.0 / max(dt, 1e-6))
            cv2.putText(display, "DiffMOT FPS %.1f | deteksi %.0f ms | TRACK %d"
                        % (fps, dt * 1000, len(online)),
                        (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
            if display.shape[1] > a.max_w:
                s = a.max_w / float(display.shape[1])
                display = cv2.resize(display, (a.max_w, int(display.shape[0] * s)))
            writer.write(display)
            if a.show:
                cv2.imshow("DiffMOT realtime", display)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

            ok, frame = cap.read()
            if not ok:
                print("Sumber selesai.")
                break
            frame_id += 1
    except KeyboardInterrupt:
        print("\nDihentikan user.")
    finally:
        tracker.dump_cache()
        cap.release()
        writer.release()
        if a.show:
            cv2.destroyAllWindows()
    print("Selesai. Video: %s (FPS rata-rata %.1f, %d frame)"
          % (a.save, fps, frame_id))
    return 0


if __name__ == "__main__":
    sys.exit(main())
