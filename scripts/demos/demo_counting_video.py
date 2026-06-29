import sys
import os
import cv2
from ultralytics import YOLO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.counting.models import Point, Line
from core.counting.counter import PeopleCounter

def main():
    video_path = r"g:\semester 6\hibah-riset\data\sample_people.mp4"
    output_path = r"g:\semester 6\hibah-riset\experiments\counting_video_demo.mp4"
    
    if not os.path.exists(video_path):
        print(f"Error: Video tidak ditemukan di {video_path}")
        return

    # Load Model (Gunakan YOLO26n yang tercepat)
    print("Memuat model YOLO26n...")
    model = YOLO("yolo26n.pt")

    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Buat Garis Virtual vertikal tepat di depan pintu (kiri layar)
    # Sesuaikan dengan letak pintu di video (sekitar 25% dari kiri)
    door_x = int(width * 0.25)
    v_line = Line(Point(door_x, 0), Point(door_x, height))
    counter = PeopleCounter(v_line)

    # Setup Video Writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print("Memproses video... Mohon tunggu (ini mungkin memakan waktu beberapa saat).")
    
    frame_count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        frame_count += 1
        
        # Jalankan tracking dengan YOLO
        # persist=True mengaktifkan sistem tracking bawaan (ByteTrack/BoT-SORT)
        results = model.track(frame, persist=True, classes=[0], verbose=False)
        
        # Gambar garis virtual vertikal
        cv2.line(frame, (int(v_line.start.x), int(v_line.start.y)), 
                 (int(v_line.end.x), int(v_line.end.y)), (255, 0, 0), 4)
        cv2.putText(frame, "GARIS PINTU", (int(v_line.start.x) + 10, int(height * 0.5)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            
            for box, track_id in zip(boxes, track_ids):
                x1, y1, x2, y2 = box
                
                # Hitung titik tengah (centroid) bagian bawah (kaki)
                # Biasanya kaki lebih akurat untuk mendeteksi persimpangan pintu
                cx = (x1 + x2) / 2
                cy = y2 
                current_point = Point(cx, cy)
                
                # Update counter
                counter.update(track_id, current_point)
                
                # Visualisasi Bounding Box dan Titik Centroid
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.circle(frame, (int(cx), int(cy)), 5, (0, 0, 255), -1)
                cv2.putText(frame, f"ID: {track_id}", (int(x1), int(y1) - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Visualisasi jejak lintasan kecil (History)
                if track_id in counter._history:
                    prev = counter._history[track_id]
                    cv2.line(frame, (int(prev.x), int(prev.y)), (int(cx), int(cy)), (0, 255, 255), 2)

        # Gambar teks Counter di layar
        status_text = f"IN: {counter.count_in}  |  OUT: {counter.count_out}"
        cv2.rectangle(frame, (20, 20), (350, 80), (0, 0, 0), -1)
        cv2.putText(frame, status_text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
        
        out.write(frame)

    cap.release()
    out.release()
    print(f"\nSelesai diproses! Video disimpan di: {output_path}")

if __name__ == '__main__':
    main()
