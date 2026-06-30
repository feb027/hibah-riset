import os
from ultralytics import YOLO

# Kita pakai gambar teater anak-anak yang paling padat
IMAGES_DIR = r"c:\projects\hibah-riset\experiments\sanity_check"
test_image = os.path.join(IMAGES_DIR, "273275,e99d80007220d4b6_verified.jpg")

models = ["yolo11n.pt", "yolov10n.pt", "yolo26n.pt"]

def main():
    print("\n--- MENGUJI OVERHEAD NMS (POST-PROCESSING) ---")
    print("Menggunakan iterasi 20x untuk mendapatkan rata-rata waktu yang stabil.")
    print("-" * 75)
    print(f"{'Model':<15} | {'Inference (ms)':<15} | {'Post-Process/NMS (ms)':<22} | {'Sifat Model'}")
    print("-" * 75)

    for model_name in models:
        # Load model secara diam-diam
        model = YOLO(model_name)
        
        # WARMUP (Panaskan model agar tidak ada lag awal)
        for _ in range(5):
            model(test_image, verbose=False)
            
        avg_inf = 0
        avg_post = 0
        iters = 20
        
        # MULAI TESTING
        for _ in range(iters):
            results = model(test_image, verbose=False)
            speed = results[0].speed
            avg_inf += speed['inference']
            avg_post += speed['postprocess']
            
        avg_inf /= iters
        avg_post /= iters
        
        sifat = "Ada NMS (Lambat)" if "11" in model_name or "8" in model_name else "NMS-Free (Cepat)"
        
        print(f"{model_name:<15} | {avg_inf:<15.2f} | {avg_post:<22.2f} | {sifat}")
    
    print("-" * 75)
    print("\nKesimpulan: Perhatikan kolom 'Post-Process/NMS'.")

if __name__ == "__main__":
    main()
