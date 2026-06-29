import sys
import os
# Memastikan modul 'core' bisa di-import dari dalam folder scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
from core.counting.models import Point, Line
from core.counting.counter import PeopleCounter

def main():
    # Gunakan gambar teater sebagai background visualisasi
    img_path = r"g:\semester 6\hibah-riset\models\Images\273275,e99d80007220d4b6.jpg"
    img = cv2.imread(img_path)
    
    # 1. Definisikan Garis Virtual Pembatas (Warna Biru)
    # Dari X=100 ke X=500, pada ketinggian Y=300
    v_line = Line(Point(100, 300), Point(540, 300))
    counter = PeopleCounter(v_line)
    
    cv2.line(img, (int(v_line.start.x), int(v_line.start.y)), (int(v_line.end.x), int(v_line.end.y)), (255, 0, 0), 4)
    cv2.putText(img, "GARIS BATAS VIRTUAL", (120, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    
    # 2. Simulasi Orang 1 (Jalan ke Bawah - Memotong Garis) -> Dihitung "IN"
    print("Mensimulasikan Orang 1 berjalan turun...")
    person1_path = [Point(200, 150), Point(200, 250), Point(200, 350)]
    for i, p in enumerate(person1_path):
        counter.update(track_id=1, current_centroid=p)
        cv2.circle(img, (int(p.x), int(p.y)), 8, (0, 255, 0), -1) # Titik Hijau
        if i > 0:
            prev = person1_path[i-1]
            cv2.line(img, (int(prev.x), int(prev.y)), (int(p.x), int(p.y)), (0, 255, 0), 3)
            
    # 3. Simulasi Orang 2 (Jalan ke Atas - Memotong Garis) -> Dihitung "OUT"
    print("Mensimulasikan Orang 2 berjalan naik...")
    person2_path = [Point(450, 450), Point(450, 350), Point(450, 180)]
    for i, p in enumerate(person2_path):
        counter.update(track_id=2, current_centroid=p)
        cv2.circle(img, (int(p.x), int(p.y)), 8, (0, 0, 255), -1) # Titik Merah
        if i > 0:
            prev = person2_path[i-1]
            cv2.line(img, (int(prev.x), int(prev.y)), (int(p.x), int(p.y)), (0, 0, 255), 3)

    # 4. Cetak Hasil Hitungan Counter Logic kita ke Layar
    status_text = f"IN: {counter.count_in}  |  OUT: {counter.count_out}"
    cv2.rectangle(img, (20, 20), (350, 80), (0, 0, 0), -1)
    cv2.putText(img, status_text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
    
    out_path = r"g:\semester 6\hibah-riset\experiments\counting_demo.jpg"
    cv2.imwrite(out_path, img)
    print(f"\nSimulasi Selesai! Visualisasi disimpan di:\n{out_path}")

if __name__ == '__main__':
    main()
