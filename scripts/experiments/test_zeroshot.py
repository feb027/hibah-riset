import os
import cv2
from ultralytics import YOLO

# Konfigurasi Path
IMAGES_DIR = r"g:\semester 6\hibah-riset\models\Images"
OUTPUT_DIR = r"g:\semester 6\hibah-riset\experiments\zeroshot"

TEST_IMAGES = [
    "273271,c9db000d5146c15.jpg",
    "273271,1c72c000a2ee47d5.jpg",
    "273275,e99d80007220d4b6.jpg"
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    models_to_test = ["yolov10n.pt", "yolo11n.pt", "yolo26n.pt"]
    
    for model_name in models_to_test:
        print(f"\n=========================================")
        print(f" Menguji Model Zero-Shot: {model_name}")
        print(f"=========================================")
        model = YOLO(model_name) 

        for img_name in TEST_IMAGES:
            img_path = os.path.join(IMAGES_DIR, img_name)
            
            if not os.path.exists(img_path):
                print(f"File tidak ditemukan: {img_path}")
                continue
                
            # Run inference (hanya deteksi kelas 0 = person)
            results = model(img_path, classes=[0], conf=0.25, verbose=False)
            
            # Ambil gambar hasil plotting
            res_plotted = results[0].plot()
            
            # Save format: nama_gambar_namamodel.jpg
            model_base = model_name.replace(".pt", "")
            img_base = img_name.replace(".jpg", "")
            out_path = os.path.join(OUTPUT_DIR, f"{img_base}_{model_base}.jpg")
            
            cv2.imwrite(out_path, res_plotted)
            
            num_detected = len(results[0].boxes)
            print(f" -> [{img_base}] berhasil mendeteksi: {num_detected} orang")

if __name__ == "__main__":
    main()
