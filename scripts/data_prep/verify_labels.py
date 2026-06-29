import os
import json
import cv2
from pathlib import Path

# Konfigurasi Path
ODGT_PATH = r"g:\semester 6\hibah-riset\models\annotation_val.odgt"
IMAGES_DIR = r"g:\semester 6\hibah-riset\models\Images"
OUTPUT_DIR = r"g:\semester 6\hibah-riset\experiments\sanity_check"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    if not os.path.exists(ODGT_PATH):
        print(f"Error: Label file tidak ditemukan di {ODGT_PATH}")
        return

    with open(ODGT_PATH, 'r') as f:
        lines = f.readlines()
        
    print(f"Total data di ODGT: {len(lines)}")
    print("Memproses 3 gambar pertama untuk Sanity Check...")

    processed_count = 0
    for line in lines:
        if processed_count >= 3:
            break
            
        data = json.loads(line)
        img_id = data['ID']
        img_path = os.path.join(IMAGES_DIR, f"{img_id}.jpg")
        
        if not os.path.exists(img_path):
            print(f"Gambar tidak ditemukan: {img_path}")
            continue
            
        img = cv2.imread(img_path)
        if img is None:
            print(f"Gagal membaca gambar: {img_path}")
            continue
            
        img_height, img_width = img.shape[:2]
        
        for gt in data.get('gtboxes', []):
            if gt['tag'] == 'person':
                # Kotak asli dari ODGT
                x, y, w, h = gt['fbox']
                
                # 1. Konversi ke YOLO format (mengikuti logika convert_crowdhuman_to_yolo.py)
                x_center = (x + w / 2.0) / img_width
                y_center = (y + h / 2.0) / img_height
                norm_w = w / img_width
                norm_h = h / img_height
                
                # Kliping batas agar tidak keluar gambar (0 s.d 1)
                x_center = max(0, min(1, x_center))
                y_center = max(0, min(1, y_center))
                norm_w = max(0, min(1, norm_w))
                norm_h = max(0, min(1, norm_h))
                
                # 2. Kembalikan dari YOLO format ke Koordinat Piksel untuk digambar
                pixel_w = int(norm_w * img_width)
                pixel_h = int(norm_h * img_height)
                pixel_xc = int(x_center * img_width)
                pixel_yc = int(y_center * img_height)
                
                x1 = pixel_xc - pixel_w // 2
                y1 = pixel_yc - pixel_h // 2
                x2 = pixel_xc + pixel_w // 2
                y2 = pixel_yc + pixel_h // 2
                
                # 3. Gambar kotak warna HIJAU (BGR)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
        out_path = os.path.join(OUTPUT_DIR, f"{img_id}_verified.jpg")
        cv2.imwrite(out_path, img)
        print(f"Tersimpan: {out_path}")
        processed_count += 1
        
    print(f"\nSelesai! Silakan buka folder {OUTPUT_DIR} untuk melihat hasilnya.")

if __name__ == "__main__":
    main()
