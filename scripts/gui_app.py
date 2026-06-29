import sys
import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.counting.models import Point
from core.counting.counter import PeopleCounter
from core.gui.drawer import LineDrawerState

class PeopleCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi People Counter Desktop - SOTA YOLO26")
        self.root.geometry("1280x800")
        self.root.configure(bg="#2c3e50")
        
        # State variables
        self.video_path = None
        self.cap = None
        print("Memuat model YOLO26n...")
        self.model = YOLO("yolo26n.pt")
        self.is_processing = False
        self.drawer_state = LineDrawerState()
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
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
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
            self.lbl_status.config(text="Status: Gambarlah garis pintu di layar (Klik Titik 1, lalu Klik Titik 2)")
            self.btn_start.config(state=tk.NORMAL)
            self.drawer_state.reset()
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

    def on_canvas_click(self, event):
        if self.is_processing or self.first_frame is None:
            return
            
        if not hasattr(self, 'ratio'):
            self.calculate_scale()
            
        # Konversi titik klik dari Layar (Canvas) ke Resolusi Asli Video
        orig_x = (event.x - self.x_offset) / self.ratio
        orig_y = (event.y - self.y_offset) / self.ratio
        
        frame_h, frame_w = self.first_frame.shape[:2]
        
        if 0 <= orig_x <= frame_w and 0 <= orig_y <= frame_h:
            self.drawer_state.add_point(orig_x, orig_y)
            self.redraw_first_frame()

    def redraw_first_frame(self):
        if self.first_frame is None:
            return
            
        frame_copy = self.first_frame.copy()
        
        if self.drawer_state.point1:
            p = self.drawer_state.point1
            cv2.circle(frame_copy, (int(p.x), int(p.y)), 10, (0, 255, 0), -1)
            
        if self.drawer_state.is_complete:
            p1 = self.drawer_state.point1
            p2 = self.drawer_state.point2
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
        if not self.drawer_state.is_complete:
            messagebox.showwarning("Belum Selesai", "Anda harus mengeklik 2 titik pada layar untuk membuat Garis Batas terlebih dahulu.")
            return
            
        self.is_processing = True
        self.btn_open.config(state=tk.DISABLED)
        self.btn_start.config(state=tk.DISABLED)
        self.lbl_status.config(text="Status: Mendeteksi dan Menghitung...", fg="#f1c40f")
        
        virtual_line = self.drawer_state.get_line()
        self.counter = PeopleCounter(virtual_line)
        
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
        
        virtual_line = self.drawer_state.get_line()
        
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
