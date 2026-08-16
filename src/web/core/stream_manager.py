"""Thread-safe, low-latency Video Stream Manager.

Mendukung berbagai sumber input video:
1. Webcam lokal (index 0, 1, dst.)
2. File video MP4 / AVI / MKV
3. Direktori sekuens gambar (MOT format)
4. Aliran jaringan IP / RTSP / HTTP (mis. Kamera HP via Tailscale)
"""
from __future__ import annotations

import os
import threading
import time
from pathlib import Path
from typing import Optional, Tuple, Union

import cv2
import numpy as np


class StreamManager:
    """Mengelola penangkapan frame secara asinkron dengan buffer nol untuk meminimalkan latensi."""

    def __init__(self, source: Union[int, str] = 0):
        self.source = source
        self.cap: Optional[cv2.VideoCapture] = None
        self._image_sequence: list[Path] = []
        self._seq_idx = 0
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._latest_frame: Optional[np.ndarray] = None
        self._frame_w = 640
        self._frame_h = 480
        self._fps = 30.0
        self._source_name = str(source)
        self._is_sequence = False

    @property
    def dimensions(self) -> Tuple[int, int]:
        return self._frame_w, self._frame_h

    @property
    def source_name(self) -> str:
        return self._source_name

    def start(self) -> bool:
        """Buka sumber video dan jalankan worker pembaca frame di background thread."""
        self._is_sequence = False
        self._is_client_feed = False
        self._image_sequence = []
        self._seq_idx = 0

        # Cek jika sumber adalah stream kamera dari browser/HP klien
        if str(self.source).lower() in ("client_upload", "browser_camera", "phone"):
            self._is_client_feed = True
            self._source_name = "Kamera Browser / HP"
            self._running = True
            print("[StreamManager] Menunggu aliran frame dari kamera browser/HP klien...")
            return True

        # Cek jika sumber adalah direktori sekuens gambar
        if isinstance(self.source, str) and os.path.isdir(self.source):
            p = Path(self.source)
            img1 = p / "img1" if (p / "img1").is_dir() else p
            self._image_sequence = sorted(img1.glob("*.jpg")) or sorted(img1.glob("*.png"))
            if self._image_sequence:
                self._is_sequence = True
                f0 = cv2.imread(str(self._image_sequence[0]))
                if f0 is not None:
                    self._frame_h, self._frame_w = f0.shape[:2]
                    self._latest_frame = f0
                self._source_name = f"Sequence: {p.name}"

        if not self._is_sequence:
            src_val = int(self.source) if isinstance(self.source, str) and self.source.isdigit() else self.source
            # Di Windows, gunakan DSHOW untuk webcam USB agar startup cepat
            if isinstance(src_val, int) and os.name == "nt":
                self.cap = cv2.VideoCapture(src_val, cv2.CAP_DSHOW)
            else:
                self.cap = cv2.VideoCapture(src_val)

            if not self.cap.isOpened():
                # Fallback ke backend default
                self.cap = cv2.VideoCapture(src_val)
                if not self.cap.isOpened():
                    print(f"[StreamManager] Tidak ada webcam fisik ({self.source}). Otomatis masuk Mode Standby (Siap terima stream Kamera HP/Browser).")
                    self._is_client_feed = True
                    self._source_name = "Kamera Browser / HP (Standby)"
                    # Buat frame placeholder standby
                    blank = np.zeros((480, 640, 3), dtype=np.uint8)
                    cv2.putText(blank, "MENUNGGU ALIRAN KAMERA HP / WEBCAM", (60, 240),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (160, 160, 160), 2, cv2.LINE_AA)
                    cv2.putText(blank, "Buka di HP / Laptop dan klik 'Ganti Sumber' -> Kamera Perangkat", (60, 275),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (100, 100, 100), 1, cv2.LINE_AA)
                    self._latest_frame = blank
                    self._running = True
                    return True

            # Set buffer size = 1 untuk mencegah delay RTSP/Webcam
            try:
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            except Exception:
                pass

            ret, f0 = self.cap.read()
            if ret and f0 is not None:
                self._frame_h, self._frame_w = f0.shape[:2]
                self._latest_frame = f0
            else:
                print(f"[StreamManager] Kamera tidak merespon frame. Masuk Mode Standby.")
                self._is_client_feed = True
                self._source_name = "Kamera Browser / HP (Standby)"
                blank = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(blank, "MENUNGGU ALIRAN KAMERA HP / WEBCAM", (60, 240),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (160, 160, 160), 2, cv2.LINE_AA)
                self._latest_frame = blank
                self._running = True
                return True

            if isinstance(src_val, int):
                self._source_name = f"Webcam {src_val}"
            elif str(src_val).startswith("http") or str(src_val).startswith("rtsp"):
                self._source_name = "IP/RTSP Stream"
            else:
                self._source_name = Path(str(src_val)).name

        self._running = True
        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()
        print(f"[StreamManager] Sumber aktif: {self._source_name} ({self._frame_w}x{self._frame_h})")
        return True

    def _capture_loop(self) -> None:
        """Loop latar belakang untuk membaca frame tercepat tanpa blocking."""
        while self._running:
            if self._is_sequence:
                if not self._image_sequence:
                    time.sleep(0.033)
                    continue
                img_path = self._image_sequence[self._seq_idx]
                f = cv2.imread(str(img_path))
                self._seq_idx = (self._seq_idx + 1) % len(self._image_sequence)
                if f is not None:
                    with self._lock:
                        self._latest_frame = f
                time.sleep(0.033)  # Simulasi ~30 FPS untuk sekuens gambar
            else:
                if self.cap is None or not self.cap.isOpened():
                    time.sleep(0.05)
                    continue
                ret, f = self.cap.read()
                if ret and f is not None:
                    with self._lock:
                        self._latest_frame = f
                else:
                    # Jika file video selesai, ulangi dari awal (looping)
                    if not isinstance(self.source, int) and not str(self.source).startswith("rtsp"):
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    time.sleep(0.01)

    def read_frame(self) -> Optional[np.ndarray]:
        """Ambil frame terbaru secara thread-safe."""
        with self._lock:
            if self._latest_frame is None:
                return None
            return self._latest_frame.copy()

    def feed_client_frame(self, frame_bgr: np.ndarray) -> None:
        """Terima frame yang dikirim langsung dari browser atau HP klien."""
        if frame_bgr is not None and frame_bgr.size > 0:
            with self._lock:
                self._latest_frame = frame_bgr
                self._frame_h, self._frame_w = frame_bgr.shape[:2]

    def set_source(self, new_source: Union[int, str]) -> bool:
        """Ganti sumber video secara dinamis saat runtime."""
        self.stop()
        self.source = new_source
        return self.start()

    def stop(self) -> None:
        """Hentikan thread penangkapan dan bebaskan perangkat keras."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        self._thread = None
        if self.cap is not None:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None
        self._latest_frame = None
