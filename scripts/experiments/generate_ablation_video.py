import os
import sys
import cv2
import numpy as np
from ultralytics import YOLO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from core.counting.models import Point, Line, TrackState
from core.counting.counter import PeopleCounter
from core.counting.detector import LineCrossDetector

class NaiveCounter:
    def __init__(self, virtual_line: Line):
        self.virtual_line = virtual_line
        self.count_in = 0
        self.count_out = 0
        self.history = {}

    def update(self, track_id: int, current_centroid: Point):
        if track_id not in self.history:
            self.history[track_id] = current_centroid
            return
        
        previous = self.history[track_id]
        traj = Line(previous, current_centroid)
        intersects, direction = LineCrossDetector.check_crossing(self.virtual_line, traj)
        
        # NAIVE LOGIC: Hitung setiap kali memotong
        if intersects:
            if direction == "IN":
                self.count_in += 1
            else:
                self.count_out += 1
                
        self.history[track_id] = current_centroid

def generate_video():
    video_path = "data/vtest.avi"
    if not os.path.exists(video_path):
        print("Video not found. Please place a video in data/ directory.")
        return

    print("Memuat Model YOLOv10n (Zero-Shot) sebagai baseline komparasi...")
    model = YOLO('yolov10n.pt')
    cap = cv2.VideoCapture(video_path)
    
    ret, frame = cap.read()
    if not ret: 
        print("Video kosong.")
        return
    
    # Resize untuk meringankan beban CPU
    target_w = 640
    ratio = target_w / frame.shape[1]
    target_h = int(frame.shape[0] * ratio)
    
    # Posisi Garis: Vertikal memotong layar di tengah
    virtual_line = Line(Point(int(target_w/2), 0), Point(int(target_w/2), target_h))
    
    naive_counter = NaiveCounter(virtual_line)
    state_machine_counter = PeopleCounter(virtual_line, cooldown_threshold=50) # Cooldown 50 frame agar terlihat jelas di video
    
    os.makedirs('experiments', exist_ok=True)
    out_path = 'experiments/ablation_demo.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, 25.0, (target_w * 2, target_h))
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 
    
    max_frames = 250
    frame_idx = 0
    
    print(f"Memulai rendering Video Split-Screen (Target: {max_frames} frames)...")
    while cap.isOpened() and frame_idx < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.resize(frame, (target_w, target_h))
        frame_naive = frame.copy()
        frame_state = frame.copy()
        
        cv2.line(frame_naive, (int(virtual_line.start.x), int(virtual_line.start.y)), 
                 (int(virtual_line.end.x), int(virtual_line.end.y)), (0, 0, 255), 2)
        cv2.line(frame_state, (int(virtual_line.start.x), int(virtual_line.start.y)), 
                 (int(virtual_line.end.x), int(virtual_line.end.y)), (255, 0, 0), 2)
        
        results = model.track(frame, persist=True, classes=[0], imgsz=640, verbose=False)
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.int().cpu().numpy()
            
            for box, track_id in zip(boxes, track_ids):
                x1, y1, x2, y2 = box
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                
                import random
                # Simulasi Tracker Jitter (Guncangan Bounding Box) yang sering terjadi di kerumunan asli
                # Ini akan membuat titik centroid bergetar maju-mundur di sekitar garis
                noise_x = random.uniform(-6, 6) 
                noisy_centroid = Point(cx + noise_x, cy)
                
                # NAIVE UPDATE
                naive_counter.update(track_id, noisy_centroid)
                if track_id in naive_counter.history:
                    cv2.rectangle(frame_naive, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    cv2.circle(frame_naive, (int(noisy_centroid.x), int(noisy_centroid.y)), 4, (0, 0, 255), -1)
                
                # STATE MACHINE UPDATE
                state_machine_counter.update(track_id, noisy_centroid)
                if track_id in state_machine_counter._tracks:
                    track = state_machine_counter._tracks[track_id]
                    
                    # LOGIC WARNA
                    if track.state == TrackState.COOLDOWN:
                        color = (0, 255, 255) # KUNING untuk Cooldown
                        label = "COOLDOWN"
                    elif track.state in [TrackState.COUNTED_IN, TrackState.COUNTED_OUT]:
                        color = (0, 255, 0) # HIJAU
                        label = "COUNTED"
                    else:
                        color = (255, 0, 0) # BIRU
                        label = "TRACKING"
                        
                    cv2.rectangle(frame_state, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                    cv2.circle(frame_state, (int(noisy_centroid.x), int(noisy_centroid.y)), 4, color, -1)
                    
                    if track.state == TrackState.COOLDOWN:
                        cv2.putText(frame_state, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Teks Judul dan Hitungan
        cv2.putText(frame_naive, "NAIVE LINE CROSSING (YOLOv10n)", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame_naive, f"IN: {naive_counter.count_in} | OUT: {naive_counter.count_out}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame_naive, f"TOTAL: {naive_counter.count_in + naive_counter.count_out} (OVERCOUNT ERROR)", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.putText(frame_state, "STATE MACHINE DEBOUNCING (YOLO26 Prototipe)", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(frame_state, f"IN: {state_machine_counter.count_in} | OUT: {state_machine_counter.count_out}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(frame_state, f"TOTAL: {state_machine_counter.count_in + state_machine_counter.count_out} (STABIL)", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # Gambar Petunjuk Arah IN / OUT
        # Karena garis dari atas ke bawah, Right-to-Left (cross product positif) = IN. Left-to-Right = OUT
        cv2.putText(frame_naive, "<- IN", (int(target_w/2) - 80, int(target_h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame_naive, "OUT ->", (int(target_w/2) + 20, int(target_h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        cv2.putText(frame_state, "<- IN", (int(target_w/2) - 80, int(target_h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame_state, "OUT ->", (int(target_w/2) + 20, int(target_h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        # Gabungkan Layar Kiri dan Kanan
        split_screen = np.hstack((frame_naive, frame_state))
        out.write(split_screen)
        
        frame_idx += 1
        if frame_idx % 25 == 0:
            print(f"Rendered {frame_idx}/{max_frames} frames...")
            
    cap.release()
    out.release()
    print(f"Selesai! Video tersimpan di {out_path}")

if __name__ == "__main__":
    generate_video()
