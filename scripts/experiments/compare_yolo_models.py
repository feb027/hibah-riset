import os
import time
import urllib.request
import pandas as pd
from ultralytics import YOLO

# Download a sample video if it doesn't exist
VIDEO_URL = "https://github.com/intel-iot-devkit/sample-videos/raw/master/people-detection.mp4"
VIDEO_PATH = "data/sample_people.mp4"
os.makedirs("data", exist_ok=True)
os.makedirs("experiments", exist_ok=True)

if not os.path.exists(VIDEO_PATH):
    print(f"Downloading sample video to {VIDEO_PATH}...")
    urllib.request.urlretrieve(VIDEO_URL, VIDEO_PATH)
    print("Download complete.")

MODELS_TO_TEST = [
    "yolov10n.pt",
    "yolov10s.pt",
    "yolo11n.pt",
    "yolo11s.pt",
    "yolo26n.pt",
    "yolo26s.pt"
]

results_data = []

print("Starting YOLO comparison on CPU...")

for model_name in MODELS_TO_TEST:
    print(f"\n--- Loading {model_name} ---")
    try:
        model = YOLO(model_name)
    except Exception as e:
        print(f"Failed to load {model_name}: {e}")
        continue
    
    print(f"Running inference for {model_name}...")
    
    # Run prediction
    start_time = time.time()
    # We set verbose=False to keep logs clean
    results = model.predict(source=VIDEO_PATH, save=False, stream=False, verbose=False, device='cpu')
    end_time = time.time()
    
    total_time = end_time - start_time
    total_frames = len(results)
    avg_fps = total_frames / total_time if total_time > 0 else 0
    
    total_people_detected = 0
    confidences = []
    
    for r in results:
        # Filter only person class (class 0 for COCO)
        boxes = r.boxes
        if boxes is not None:
            person_boxes = boxes[boxes.cls == 0]
            total_people_detected += len(person_boxes)
            confidences.extend(person_boxes.conf.cpu().numpy().tolist())
    
    avg_conf = sum(confidences) / len(confidences) if confidences else 0
    
    print(f"Results for {model_name}:")
    print(f"  Frames Processed: {total_frames}")
    print(f"  Total Time: {total_time:.2f}s")
    print(f"  Avg FPS: {avg_fps:.2f}")
    print(f"  Total People Detections (across all frames): {total_people_detected}")
    print(f"  Avg Confidence: {avg_conf:.4f}")
    
    results_data.append({
        "Model": model_name,
        "Total_Frames": total_frames,
        "Total_Time_s": total_time,
        "Avg_FPS": avg_fps,
        "Total_Detections": total_people_detected,
        "Avg_Confidence": avg_conf
    })

# Save results to CSV
df = pd.DataFrame(results_data)
output_csv = "experiments/yolo_comparison_results.csv"
df.to_csv(output_csv, index=False)
print(f"\nComparison complete. Results saved to {output_csv}")
