import sys
import os
import cv2
import argparse
from ultralytics import YOLO

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.counting.models import Point
from core.counting.counter import PeopleCounter
from core.gui.drawer import LineDrawerState

def main():
    parser = argparse.ArgumentParser(description="Interactive People Counting Demo")
    parser.add_argument("--video", type=str, default=r"g:\semester 6\hibah-riset\data\15546948_1080_1920_50fps.mp4", help="Path to input video")
    args = parser.parse_args()
    
    video_path = args.video
    if not os.path.exists(video_path):
        print(f"Error: Video tidak ditemukan di {video_path}")
        return

    # 1. Buka Video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Tidak dapat membuka video.")
        return
        
    success, first_frame = cap.read()
    if not success:
        print("Error: Tidak dapat membaca frame pertama.")
        return
        
    # Resize untuk tampilan GUI yang lebih nyaman jika video terlalu besar (misal 1080p -> 720p)
    # Tapi kita butuh proporsi asli untuk perhitungan. Mari kita resize tampilannya saja 
    # atau biarkan aslinya jika muat. Untuk aman, kita tampilkan apa adanya.
    display_frame = first_frame.copy()
    
    # 2. Inisialisasi State GUI
    drawer_state = LineDrawerState()
    
    # Callback Mouse OpenCV
    def draw_line(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            drawer_state.add_point(x, y)
            
    window_name = "GUI Interaktif - Gambar Garis Pintu (Klik 2x, lalu tekan ENTER)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, draw_line)
    
    print("==================================================")
    print("MODE GUI INTERAKTIF AKTIF")
    print("1. Klik KIRI di titik pertama untuk awal garis.")
    print("2. Klik KIRI di titik kedua untuk akhir garis.")
    print("3. Tekan tombol ENTER untuk mulai proses tracking.")
    print("4. Jika salah klik, klik lagi untuk mereset.")
    print("==================================================")

    # 3. Loop Interaktif Menunggu Garis Digambar
    while True:
        temp_frame = display_frame.copy()
        
        # Tampilkan instruksi di layar
        cv2.putText(temp_frame, "KLIK 2 TITIK UNTUK MEMBUAT GARIS.", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv2.putText(temp_frame, "TEKAN 'ENTER' JIKA SUDAH SELESAI.", (20, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        
        # Gambar titik/garis yang sedang dibuat
        if drawer_state.point1:
            cv2.circle(temp_frame, (int(drawer_state.point1.x), int(drawer_state.point1.y)), 5, (0, 255, 0), -1)
        
        if drawer_state.is_complete:
            cv2.circle(temp_frame, (int(drawer_state.point2.x), int(drawer_state.point2.y)), 5, (0, 255, 0), -1)
            cv2.line(temp_frame, 
                     (int(drawer_state.point1.x), int(drawer_state.point1.y)), 
                     (int(drawer_state.point2.x), int(drawer_state.point2.y)), 
                     (255, 0, 0), 3)
            
        cv2.imshow(window_name, temp_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 13:  # 13 adalah tombol ENTER
            if drawer_state.is_complete:
                break
            else:
                print("Garis belum selesai dibuat! Butuh 2 titik.")
        elif key == 27: # 27 adalah tombol ESC (Keluar)
            print("Dibatalkan oleh pengguna.")
            cap.release()
            cv2.destroyAllWindows()
            return
            
    cv2.destroyWindow(window_name)
    virtual_line = drawer_state.get_line()
    print(f"Garis virtual berhasil disetel dari {virtual_line.start} ke {virtual_line.end}")

    # 4. Inisialisasi Counter dan YOLO
    counter = PeopleCounter(virtual_line)
    print("Memuat model YOLO26n...")
    model = YOLO("yolo26n.pt")
    
    # Inisialisasi output video
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    out_path = r"g:\semester 6\hibah-riset\experiments\interactive_demo_output.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    print("\nMemulai pemrosesan secara Real-Time. Tekan 'q' untuk berhenti.")
    
    # 5. Loop Pemrosesan Video
    result_window = "Hasil Tracking Real-Time"
    cv2.namedWindow(result_window, cv2.WINDOW_NORMAL)
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        # Tracking YOLO
        results = model.track(frame, persist=True, classes=[0], verbose=False)
        
        # Gambar garis buatan user
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
                cy = y2  # Titik kaki
                
                counter.update(track_id, Point(cx, cy))
                
                # Visualisasi
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.circle(frame, (int(cx), int(cy)), 5, (0, 0, 255), -1)
                
                if track_id in counter._history:
                    prev = counter._history[track_id]
                    cv2.line(frame, (int(prev.x), int(prev.y)), (int(cx), int(cy)), (0, 255, 255), 2)

        # Draw Counter
        status_text = f"IN: {counter.count_in}  |  OUT: {counter.count_out}"
        cv2.rectangle(frame, (20, 20), (350, 80), (0, 0, 0), -1)
        cv2.putText(frame, status_text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
        
        out.write(frame)
        cv2.imshow(result_window, frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Dihentikan secara manual.")
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"\nSelesai! Hasil akhir disimpan di: {out_path}")

if __name__ == '__main__':
    main()
