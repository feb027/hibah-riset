import os
import argparse
from ultralytics import YOLO

def train_model(model_variant, data_yaml, epochs=50, batch_size=32, imgsz=640, resume=False):
    """
    Script to fine-tune YOLO model on CrowdHuman dataset.
    Optimized for high-end GPUs like RTX 4090.
    """
    print(f"=====================================================")
    print(f" Memulai Training untuk {model_variant}")
    print(f" Epochs: {epochs} | Batch: {batch_size} | Image Size: {imgsz}")
    print(f"=====================================================")
    
    # [FITUR 1] Integrasi Weights & Biases (W&B)
    try:
        import wandb
        # Inisialisasi W&B (Jika belum login, akan diminta API key saat dijalankan)
        wandb.init(project="hibah-riset-yolo", name=f"run_{model_variant}")
        print("✅ Weights & Biases logging aktif. Pantau grafik training lewat browser!")
    except ImportError:
        print("⚠️  Tip: Install 'wandb' (pip install wandb) untuk memantau grafik training secara real-time lewat HP!")

    # [FITUR 2] Resume Training
    if resume:
        last_weights_path = f"runs/train/crowdhuman_{model_variant.replace('.pt', '')}/weights/last.pt"
        if os.path.exists(last_weights_path):
            print(f"🔄 Resume aktif: Melanjutkan training dari {last_weights_path}...")
            model = YOLO(last_weights_path)
        else:
            print(f"❌ File {last_weights_path} tidak ditemukan! Memulai training dari awal (scratch)...")
            model = YOLO(model_variant)
            resume = False # Batal resume karena file tidak ada
    else:
        model = YOLO(model_variant)
    
    # Mulai proses training
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        batch=batch_size,
        imgsz=imgsz,
        device=0, # Gunakan GPU 0 (RTX 4090)
        workers=8, 
        optimizer='auto', 
        patience=10, 
        project='runs/train',
        name=f"crowdhuman_{model_variant.replace('.pt', '')}",
        resume=resume, # Parameter ultralytics untuk melanjutkan epoch terakhir
        # Augmentasi khusus untuk kerumunan
        mosaic=1.0, 
        mixup=0.1,
        copy_paste=0.1
    )
    
    print(f"\n[SELESAI] Training {model_variant} berhasil!")
    print(f"File bobot terbaik tersimpan di: runs/train/crowdhuman_{model_variant.replace('.pt', '')}/weights/best.pt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script Training YOLO untuk RTX 4090")
    parser.add_argument("--model", type=str, default="yolo26n.pt", help="Varian model awal (yolo26n.pt, yolo26s.pt)")
    parser.add_argument("--data", type=str, default="../../data/crowdhuman.yaml", help="Path ke file data.yaml")
    parser.add_argument("--epochs", type=int, default=50, help="Jumlah epochs")
    parser.add_argument("--batch", type=int, default=32, help="Ukuran batch (RTX 4090 kuat di 32 atau 64)")
    parser.add_argument("--resume", action="store_true", help="Lanjutkan training jika sempat terputus (mati lampu, error, dll)")
    
    args = parser.parse_args()
    
    train_model(
        model_variant=args.model,
        data_yaml=args.data,
        epochs=args.epochs,
        batch_size=args.batch,
        resume=args.resume
    )
