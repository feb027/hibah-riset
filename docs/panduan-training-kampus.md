# Panduan Persiapan dan Training di PC Kampus (RTX 4090)

Panduan ini berisi urutan perintah (*commands*) yang harus dieksekusi dari awal sampai *training* berjalan.

## 0. Prasyarat (Cara Download via SSH dari Hugging Face)
Kabar baik! Karena Anda menemukan *mirror* datasetnya di Hugging Face (`sshao0516/CrowdHuman`), Anda **bisa** men-downloadnya langsung lewat terminal (SSH) di PC kampus. Tidak perlu repot memindah file dari laptop.

Di terminal PC Kampus, jalankan:
```bash
# Install Hugging Face CLI jika belum ada
pip install -U "huggingface_hub[cli]"

# Buat folder target
mkdir -p hibah-riset/data/raw/crowdhuman
cd hibah-riset/data/raw/crowdhuman

# Download dataset langsung dari Hugging Face
huggingface-cli download sshao0516/CrowdHuman --repo-type dataset --local-dir .
```
*(Perintah di atas akan men-download semua file `.zip` dan `.odgt` persis seperti yang ada di screenshot Anda langsung ke server kampus dengan kecepatan tinggi).*

---

## 1. Persiapan Repository dan Environment
Buka Terminal / Command Prompt / PowerShell di PC kampus.

```bash
# 1. Masuk ke folder kerja dan pull update terbaru dari repo
cd path/ke/hibah-riset
git pull origin main

# 2. Buat virtual environment agar library tidak berantakan
python -m venv yolo_env

# 3. Aktifkan environment (Pilih salah satu)
yolo_env\Scripts\activate      # Untuk Windows
# source yolo_env/bin/activate # Untuk Linux/Ubuntu

# 4. Install seluruh kebutuhan library (sudah mencakup Ultralytics/YOLO)
pip install -r requirements.txt
```

---

## 2. Ekstrak dan Konversi Dataset
Karena data dari CrowdHuman masih berformat zip dan labelnya `.odgt`, kita harus mengekstrak dan mengubahnya ke format teks YOLO.

```bash
# 1. Jalankan script ekstrak (Pastikan zip dan odgt ada di data/raw/crowdhuman)
python scripts/download_crowdhuman.py --raw-dir data/raw/crowdhuman

# 2. Konversi Anotasi Train ke YOLO format
python scripts/convert_crowdhuman_to_yolo.py --odgt data/raw/crowdhuman/extracted/annotation_train.odgt --images-dir data/raw/crowdhuman/extracted/CrowdHuman_train --output-dir data/processed/crowdhuman/labels/train

# 3. Konversi Anotasi Val ke YOLO format
python scripts/convert_crowdhuman_to_yolo.py --odgt data/raw/crowdhuman/extracted/annotation_val.odgt --images-dir data/raw/crowdhuman/extracted/CrowdHuman_val --output-dir data/processed/crowdhuman/labels/val
```

> **PENTING:** Pastikan Anda menyalin atau memindahkan file gambar (`.jpg`) dari folder `extracted` agar tersusun sejajar dengan folder `labels`. YOLO membaca struktur yang setara. Misalnya, buat folder `data/processed/crowdhuman/images/train` dan pindahkan semua gambar train ke sana.

---

## 3. Siapkan Konfigurasi `dataset.yaml`
Buat file teks baru bernama `dataset.yaml` dan simpan di folder `configs/`.

```yaml
# configs/dataset.yaml
# GANTI BAGIAN INI DENGAN PATH ABSOLUT DI PC KAMPUS!
path: C:\Users\NamaUser\Desktop\hibah-riset\data\processed\crowdhuman

train: images/train
val: images/val

names:
  0: person
```

---

## 4. Eksekusi Training (Skenario A)
Jika environment aktif, data sudah dikonversi, dan `dataset.yaml` siap, jalankan perintah ini:

```bash
yolo train data=configs/dataset.yaml model=yolov10n.pt epochs=100 imgsz=640 batch=32 device=0
```

**Tips Argumen:**
- `model=yolov10n.pt`: Menggunakan bobot awal YOLOv10 Nano. Bisa diganti ke versi *small* (`yolov10s.pt`) atau YOLO26 jika didukung.
- `batch=32`: Bisa dinaikkan ke `64` jika VRAM 24GB pada RTX 4090 sanggup menampungnya, akan mempercepat waktu per epoch.
- Jika dirasa kurang lama, ubah `epochs` ke `200` atau `300`. Fitur *Early Stopping* otomatis bekerja jika performa mentok.

Semoga berhasil! Pantau output CLI-nya, terutama metrik `mAP50-95` yang merupakan tolok ukur utama kompetensi detektor.
