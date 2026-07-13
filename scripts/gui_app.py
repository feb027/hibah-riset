import sys
import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.counting.models import Point, Polygon
from core.counting.counter import PeopleCounter
from core.gui.drawer import LineDrawerState, PolygonDrawerState

class PeopleCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi People Counter Desktop - SOTA YOLO26")
        self.root.geometry("1280x800")
        self.root.configure(bg="#2c3e50")
        
        # State variables
        self.video_path = None
        self.cap = None
        print("Memuat model YOLOv10n (untuk pengujian hari ini)...")
        self.model = YOLO("yolov10n.pt")
        self.is_processing = False
        self.poly_drawer = PolygonDrawerState()
        self.line_drawer = LineDrawerState()
        self.counter = None
        self.first_frame = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Panel Atas (Kontrol)
        top_frame = tk.Frame(self.root, bg="#34495e", pady=15)
        top_frame.pack(fill=tk.X)
        
        self.btn_open = tk.Button(top_frame, text="📁 1. Pilih Video", font=("Segoe UI", 12, "bold"), 
                                  command=self.open_video, bg="#3498db", fg="white", padx=10, cursor="hand2")
        self.btn_open.pack(side=tk.LEFT, padx=20)
        
        self.btn_start = tk.Button(top_frame, text="▶ 2. Mulai Hitung", font=("Segoe UI", 12, "bold"), 
                                   command=self.start_processing, bg="#e74c3c", fg="white", padx=10, state=tk.DISABLED, cursor="hand2")
        self.btn_start.pack(side=tk.LEFT, padx=10)
        
        self.lbl_status = tk.Label(top_frame, text="Status: Silakan Pilih Video", font=("Segoe UI", 12, "italic"), bg="#34495e", fg="#ecf0f1")
        self.lbl_status.pack(side=tk.LEFT, padx=30)
        
        # Panel Statistik (Hitungan IN/OUT)
        stats_frame = tk.Frame(self.root, bg="#2c3e50", pady=10)
        stats_frame.pack(fill=tk.X)
        
        self.lbl_in = tk.Label(stats_frame, text="IN: 0", font=("Consolas", 24, "bold"), bg="#2c3e50", fg="#2ecc71")
        self.lbl_in.pack(side=tk.LEFT, padx=60)
        
        self.lbl_out = tk.Label(stats_frame, text="OUT: 0", font=("Consolas", 24, "bold"), bg="#2c3e50", fg="#e74c3c")
        self.lbl_out.pack(side=tk.LEFT, padx=60)
        
        # Canvas Layar Utama
        self.canvas = tk.Canvas(self.root, bg="#1a252f", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Binding Klik Mouse
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        
        # Update canvas ketika window di-resize
        self.root.bind("<Configure>", self.on_resize)
        
    def open_video(self):
        self.video_path = filedialog.askopenfilename(
            title="Pilih Video", 
            filetypes=[("Video Files", "*.mp4 *.avi *.mkv"), ("All Files", "*.*")]
        )
        if not self.video_path:
            return
            
        if self.cap is not None:
            self.cap.release()
            
        self.cap = cv2.VideoCapture(self.video_path)
        success, frame = self.cap.read()
        
        if success:
            self.lbl_status.config(text="Status: [Tahap 1] Klik kiri untuk membuat Area Poligon ROI. Klik kanan jika selesai.")
            self.poly_drawer.reset()
            self.line_drawer.reset()
            self.btn_start.config(state=tk.DISABLED)
            self.first_frame = frame
            self.display_frame(frame)
        else:
            messagebox.showerror("Error", "Gagal membaca format video tersebut.")

    def on_resize(self, event):
        # Update skala saat canvas berubah ukuran
        if event.widget == self.canvas and not self.is_processing and self.first_frame is not None:
            self.calculate_scale()
            self.redraw_first_frame()

    def calculate_scale(self):
        self.canvas.update()
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        
        if canvas_w <= 1 or canvas_h <= 1:
            canvas_w, canvas_h = 1000, 600
            
        frame_h, frame_w = self.first_frame.shape[:2]
        
        # Hitung rasio untuk fit dalam kanvas
        self.ratio = min(canvas_w / frame_w, canvas_h / frame_h)
        self.scaled_w = int(frame_w * self.ratio)
        self.scaled_h = int(frame_h * self.ratio)
        
        # Hitung titik mulai (agar posisinya ke tengah)
        self.x_offset = (canvas_w - self.scaled_w) // 2
        self.y_offset = (canvas_h - self.scaled_h) // 2

    def on_left_click(self, event):
        if self.is_processing or self.first_frame is None:
            return
            
        if not hasattr(self, 'ratio'):
            self.calculate_scale()
            
        orig_x = (event.x - self.x_offset) / self.ratio
        orig_y = (event.y - self.y_offset) / self.ratio
        
        frame_h, frame_w = self.first_frame.shape[:2]
        if 0 <= orig_x <= frame_w and 0 <= orig_y <= frame_h:
            if not self.poly_drawer.is_complete:
                self.poly_drawer.add_point(orig_x, orig_y)
            else:
                self.line_drawer.add_point(orig_x, orig_y)
                if self.line_drawer.is_complete:
                    self.lbl_status.config(text="Status: Area dan Garis siap! Klik 'Mulai Hitung'.")
                    self.btn_start.config(state=tk.NORMAL)
                    
            self.redraw_first_frame()

    def on_right_click(self, event):
        if self.is_processing or self.first_frame is None:
            return
            
        if not self.poly_drawer.is_complete and len(self.poly_drawer.points) >= 3:
            self.poly_drawer.finish()
            self.lbl_status.config(text="Status: [Tahap 2] Gambarlah garis pintu (Klik 2 titik di dalam poligon).")
            self.redraw_first_frame()
        elif not self.poly_drawer.is_complete:
            messagebox.showwarning("Belum Selesai", "Area poligon minimal butuh 3 titik!")

    def redraw_first_frame(self):
        if self.first_frame is None:
            return
            
        frame_copy = self.first_frame.copy()
        
        # Gambar Poligon
        if len(self.poly_drawer.points) > 0:
            import numpy as np
            pts = np.array([[int(p.x), int(p.y)] for p in self.poly_drawer.points], np.int32)
            pts = pts.reshape((-1, 1, 2))
            if self.poly_drawer.is_complete:
                cv2.polylines(frame_copy, [pts], isClosed=True, color=(0, 255, 255), thickness=2)
                
                # Buat efek gelap semi-transparan (bukan hitam pekat) di luar poligon
                overlay = np.zeros_like(frame_copy)
                cv2.fillPoly(overlay, [pts], (255, 255, 255))
                # Kurangi kecerahan di luar area sebesar 40%
                frame_copy = np.where(overlay == (255, 255, 255), frame_copy, cv2.addWeighted(frame_copy, 0.6, overlay, 0, 0))
            else:
                cv2.polylines(frame_copy, [pts], isClosed=False, color=(0, 255, 255), thickness=2)
                for p in self.poly_drawer.points:
                    cv2.circle(frame_copy, (int(p.x), int(p.y)), 6, (0, 255, 255), -1)
        
        # Gambar Garis
        if self.line_drawer.point1:
            p = self.line_drawer.point1
            cv2.circle(frame_copy, (int(p.x), int(p.y)), 10, (0, 255, 0), -1)
            
        if self.line_drawer.is_complete:
            p1 = self.line_drawer.point1
            p2 = self.line_drawer.point2
            cv2.circle(frame_copy, (int(p2.x), int(p2.y)), 10, (0, 255, 0), -1)
            cv2.line(frame_copy, (int(p1.x), int(p1.y)), (int(p2.x), int(p2.y)), (255, 0, 0), 4)
            
        self.display_frame(frame_copy)

    def display_frame(self, frame):
        if not hasattr(self, 'ratio'):
            self.calculate_scale()
            
        # Gunakan cv2.resize agar hasil mutlak sesuai dengan perhitungan matematis GUI
        frame_resized = cv2.resize(frame, (self.scaled_w, self.scaled_h))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        
        img = Image.fromarray(frame_rgb)
        self.photo = ImageTk.PhotoImage(image=img)
        
        self.canvas.delete("all")
        self.canvas.create_image(self.x_offset, self.y_offset, image=self.photo, anchor=tk.NW)

    def start_processing(self):
        if not self.poly_drawer.is_complete or not self.line_drawer.is_complete:
            messagebox.showwarning("Belum Selesai", "Selesaikan gambar area Poligon dan Garis batas terlebih dahulu.")
            return
            
        self.is_processing = True
        self.btn_open.config(state=tk.DISABLED)
        self.btn_start.config(state=tk.DISABLED)
        self.lbl_status.config(text="Status: Mendeteksi dan Menghitung...", fg="#f1c40f")
        
        virtual_line = self.line_drawer.get_line()
        roi_polygon = self.poly_drawer.get_polygon()
        
        # Pass the ROI polygon to the PeopleCounter
        self.counter = PeopleCounter(virtual_line=virtual_line, roi=roi_polygon)
        
        self.process_next_frame()

    def process_next_frame(self):
        if not self.is_processing:
            return
            
        success, frame = self.cap.read()
        if not success:
            self.lbl_status.config(text="Status: Video Selesai", fg="#2ecc71")
            self.is_processing = False
            self.btn_open.config(state=tk.NORMAL)
            messagebox.showinfo("Selesai", "Pemrosesan video selesai!")
            return
            
        # PENTING: Tuning SOTA YOLO26 untuk Kerumunan Ekstrem (Resolusi Tinggi & Ambang Batas Rendah)
        # imgsz=1080 memaksa SOTA melihat pixel kecil
        # conf=0.15 agar tidak menghapus orang-orang yang tertutup
        results = self.model.track(frame, persist=True, classes=[0], conf=0.15, imgsz=1088, verbose=False)
        
        virtual_line = self.line_drawer.get_line()
        
        # Gambar Poligon ROI
        import numpy as np
        pts = np.array([[int(p.x), int(p.y)] for p in self.poly_drawer.points], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 255), thickness=2)
        
        # Beri efek gelap semi-transparan (bukan hitam pekat) di luar ROI
        overlay = np.zeros_like(frame)
        cv2.fillPoly(overlay, [pts], (255, 255, 255))
        frame = np.where(overlay == (255, 255, 255), frame, cv2.addWeighted(frame, 0.6, overlay, 0, 0))
        
        # Gambar garis
        cv2.line(frame, 
                 (int(virtual_line.start.x), int(virtual_line.start.y)), 
                 (int(virtual_line.end.x), int(virtual_line.end.y)), 
                 (255, 0, 0), 4)
                 
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            
            for box, track_id in zip(boxes, track_ids):
                x1, y1, x2, y2 = box
                cx = (x1 + x2) / 2
                cy = y2 
                
                self.counter.update(track_id, Point(cx, cy))
                
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.circle(frame, (int(cx), int(cy)), 5, (0, 0, 255), -1)
                
                if track_id in self.counter._tracks:
                    track = self.counter._tracks[track_id]
                    if len(track.history) >= 2:
                        prev = track.history[-2]
                        cv2.line(frame, (int(prev.x), int(prev.y)), (int(cx), int(cy)), (0, 255, 255), 2)
                    
        # Update UI Angka
        self.lbl_in.config(text=f"IN: {self.counter.count_in}")
        self.lbl_out.config(text=f"OUT: {self.counter.count_out}")
        
        self.display_frame(frame)
        
        # Render frame selanjutnya setelah jeda 1ms agar UI tidak membeku
        self.root.after(1, self.process_next_frame)

if __name__ == "__main__":
    root = tk.Tk()
    app = PeopleCounterApp(root)
    root.mainloop()
