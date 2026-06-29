import os
from ultralytics import YOLO
import matplotlib.pyplot as plt

IMAGES_DIR = r"g:\semester 6\hibah-riset\models\Images"
test_image = os.path.join(IMAGES_DIR, "273275,e99d80007220d4b6.jpg")
OUTPUT_PLOT = r"g:\semester 6\hibah-riset\experiments\resolusi_scaling.png"

def main():
    resolutions = [256, 320, 416, 480, 512, 640]
    models_to_test = ["yolov10n.pt", "yolo11n.pt", "yolo26n.pt"]
    
    # Dictionaries untuk menyimpan hasil tiap model
    fps_results = {m: [] for m in models_to_test}
    det_results = {m: [] for m in models_to_test}
    
    for model_name in models_to_test:
        print(f"\n--- Menguji Model: {model_name} ---")
        model = YOLO(model_name)
        
        # Warmup
        for _ in range(3):
            model(test_image, imgsz=640, verbose=False)
            
        for res in resolutions:
            iters = 5
            total_time = 0
            
            for _ in range(iters):
                results = model(test_image, imgsz=res, conf=0.25, verbose=False)
                # Total pipeline time
                total_time += results[0].speed['inference'] + results[0].speed['preprocess'] + results[0].speed['postprocess']
                
            avg_time = total_time / iters
            fps = 1000.0 / avg_time
            
            res_single = model(test_image, imgsz=res, conf=0.25, verbose=False)
            det_count = len(res_single[0].boxes)
            
            fps_results[model_name].append(fps)
            det_results[model_name].append(det_count)
            print(f"Resolusi {res}x{res} -> Detections: {det_count:2d} orang | FPS: {fps:.1f}")

    # Membuat Grafik Komparasi
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    colors = ['tab:blue', 'tab:orange', 'tab:green']
    markers = ['o', 's', '^']
    labels = ['YOLOv10n', 'YOLO11n', 'YOLO26n']

    # Subplot 1: FPS (Kecepatan)
    ax1.set_title("Kecepatan Pemrosesan (FPS) vs Resolusi", fontweight='bold')
    ax1.set_xlabel("Input Resolution (Pixels)")
    ax1.set_ylabel("FPS (Lebih tinggi lebih cepat)")
    for i, model_name in enumerate(models_to_test):
        ax1.plot(resolutions, fps_results[model_name], marker=markers[i], color=colors[i], linewidth=2, label=labels[i])
    ax1.axhline(y=30, color='red', linestyle='--', alpha=0.5, label='Batas Aman (30 FPS)')
    ax1.grid(True, alpha=0.4, linestyle='--')
    ax1.legend()
    
    # Subplot 2: Detections (Akurasi Kerumunan)
    ax2.set_title("Kemampuan Deteksi vs Resolusi", fontweight='bold')
    ax2.set_xlabel("Input Resolution (Pixels)")
    ax2.set_ylabel("Total Deteksi Orang (Lebih banyak lebih baik)")
    for i, model_name in enumerate(models_to_test):
        ax2.plot(resolutions, det_results[model_name], marker=markers[i], color=colors[i], linewidth=2, label=labels[i])
    ax2.grid(True, alpha=0.4, linestyle='--')
    ax2.legend()

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT, dpi=300, bbox_inches='tight')
    print(f"\nSelesai! Grafik Komparasi disimpan di: {OUTPUT_PLOT}")

if __name__ == "__main__":
    main()
