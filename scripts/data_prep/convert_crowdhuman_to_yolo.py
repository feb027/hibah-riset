import json
import os
import argparse
from pathlib import Path
from PIL import Image

def convert_odgt_to_yolo(odgt_path, images_dir, output_labels_dir):
    os.makedirs(output_labels_dir, exist_ok=True)
    
    with open(odgt_path, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        data = json.loads(line)
        img_id = data['ID']
        
        # Open image to get dimensions
        img_path = Path(images_dir) / f"{img_id}.jpg"
        if not img_path.exists():
            continue
            
        with Image.open(img_path) as img:
            img_width, img_height = img.size
            
        label_path = Path(output_labels_dir) / f"{img_id}.txt"
        
        with open(label_path, 'w') as f_label:
            for gt in data.get('gtboxes', []):
                if gt['tag'] == 'person':
                    # We use fbox (full body box) as the standard for people counting
                    # Format is [x, y, w, h] (top-left x, y)
                    x, y, w, h = gt['fbox']
                    
                    # Convert to YOLO format (center x, center y, w, h) normalized
                    x_center = (x + w / 2.0) / img_width
                    y_center = (y + h / 2.0) / img_height
                    norm_w = w / img_width
                    norm_h = h / img_height
                    
                    # Ensure values are between 0 and 1
                    x_center = max(0, min(1, x_center))
                    y_center = max(0, min(1, y_center))
                    norm_w = max(0, min(1, norm_w))
                    norm_h = max(0, min(1, norm_h))
                    
                    # Class 0 is person
                    f_label.write(f"0 {x_center:.6f} {y_center:.6f} {norm_w:.6f} {norm_h:.6f}\n")
                    
    print(f"Processed {len(lines)} images from {odgt_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert CrowdHuman ODGT to YOLO format")
    parser.add_argument("--odgt", type=str, required=True, help="Path to ODGT file")
    parser.add_argument("--images-dir", type=str, required=True, help="Path to directory containing images")
    parser.add_argument("--output-dir", type=str, required=True, help="Path to output labels directory")
    args = parser.parse_args()
    
    convert_odgt_to_yolo(args.odgt, args.images_dir, args.output_dir)

if __name__ == "__main__":
    main()
