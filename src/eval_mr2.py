"""Evaluasi deteksi dengan protokol CrowdHuman: MR^-2 dan AP@0.5.

Melengkapi src/eval_mAP.py yang memakai protokol COCO. Dua perbedaan pokok:

1. **Penanganan ignore region.** CrowdHuman menandai sebagian kotak `person`
   dengan `extra.ignore == 1` untuk region yang terlalu ambigu dinilai. Protokol
   resminya memperlakukan kotak itu sebagai *netral*: tidak wajib dideteksi, dan
   deteksi yang jatuh di atasnya tidak dihitung sebagai false positive. Ini
   berbeda dari sekadar menghapusnya dari ground truth - kalau hanya dihapus,
   deteksi di region itu justru berbalik menjadi false positive dan model
   dihukum dua kali.

2. **Metrik MR^-2** (*log-average miss rate*, Dollar et al.). Memetakan miss
   rate terhadap false positive per image (FPPI), lalu merata-ratakan secara
   logaritmik pada sembilan titik FPPI antara 0,01 dan 1,0. Nilai lebih kecil
   lebih baik - kebalikan dari mAP.

   MR^-2 lebih cocok untuk penelitian people counting daripada mAP karena
   menjawab langsung pertanyaan operasionalnya: berapa banyak orang yang
   terlewat pada tingkat alarm palsu yang masih dapat diterima. Orang yang
   terlewat itulah sumber under-count.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

__all__ = ["load_odgt_ground_truth", "evaluate_detections", "FPPI_REFERENCE_POINTS"]

# Sembilan titik FPPI berjarak logaritmik, sesuai protokol Caltech/CrowdHuman.
FPPI_REFERENCE_POINTS = np.logspace(-2.0, 0.0, 9)


def load_odgt_ground_truth(odgt_path, exclude_ignore_from_gt=True):
    """Baca .odgt menjadi {image_id: {"boxes": ndarray, "ignore": ndarray}}.

    Kotak dikembalikan dalam format xyxy. Kotak bertanda ignore dipisahkan ke
    kunci "ignore" agar dapat diperlakukan netral saat pencocokan, bukan sebagai
    target yang wajib ditemukan.
    """
    ground_truth = {}

    with open(odgt_path, "r") as f:
        for line in f:
            record = json.loads(line)
            positives, ignored = [], []

            for gt in record.get("gtboxes", []):
                if gt["tag"] != "person":
                    # Tag selain person (mis. "mask") adalah region ignore bawaan.
                    x, y, w, h = gt["fbox"]
                    ignored.append([x, y, x + w, y + h])
                    continue

                x, y, w, h = gt["fbox"]
                box = [x, y, x + w, y + h]
                is_ignored = gt.get("extra", {}).get("ignore", 0) == 1
                if is_ignored and exclude_ignore_from_gt:
                    ignored.append(box)
                else:
                    positives.append(box)

            ground_truth[record["ID"]] = {
                "boxes": np.array(positives, dtype=np.float64).reshape(-1, 4),
                "ignore": np.array(ignored, dtype=np.float64).reshape(-1, 4),
            }

    return ground_truth


def _iou_matrix(boxes_a, boxes_b):
    """IoU berpasangan antara dua himpunan kotak xyxy."""
    if len(boxes_a) == 0 or len(boxes_b) == 0:
        return np.zeros((len(boxes_a), len(boxes_b)))

    lt = np.maximum(boxes_a[:, None, :2], boxes_b[None, :, :2])
    rb = np.minimum(boxes_a[:, None, 2:], boxes_b[None, :, 2:])
    wh = np.clip(rb - lt, 0, None)
    intersection = wh[..., 0] * wh[..., 1]

    area_a = np.prod(np.clip(boxes_a[:, 2:] - boxes_a[:, :2], 0, None), axis=1)
    area_b = np.prod(np.clip(boxes_b[:, 2:] - boxes_b[:, :2], 0, None), axis=1)
    union = area_a[:, None] + area_b[None, :] - intersection

    return np.where(union > 0, intersection / np.maximum(union, 1e-9), 0.0)


def _ioa_matrix(boxes_a, boxes_b):
    """Irisan dibagi luas kotak A (*intersection over area*).

    Dipakai untuk mencocokkan deteksi dengan region ignore. IoU tidak cocok di
    sini karena region ignore sering jauh lebih besar daripada satu deteksi,
    sehingga IoU-nya kecil meskipun deteksi sepenuhnya berada di dalam region.
    """
    if len(boxes_a) == 0 or len(boxes_b) == 0:
        return np.zeros((len(boxes_a), len(boxes_b)))

    lt = np.maximum(boxes_a[:, None, :2], boxes_b[None, :, :2])
    rb = np.minimum(boxes_a[:, None, 2:], boxes_b[None, :, 2:])
    wh = np.clip(rb - lt, 0, None)
    intersection = wh[..., 0] * wh[..., 1]

    area_a = np.prod(np.clip(boxes_a[:, 2:] - boxes_a[:, :2], 0, None), axis=1)
    return intersection / np.maximum(area_a[:, None], 1e-9)


def _match_image(det_boxes, det_scores, gt_boxes, ignore_boxes, iou_thr, ioa_thr):
    """Cocokkan deteksi satu citra. Mengembalikan (skor, label) per deteksi.

    Label: 1 = true positive, 0 = false positive, -1 = jatuh di region ignore
    (dikeluarkan dari perhitungan, tidak dihukum maupun dihargai).
    """
    order = np.argsort(-det_scores)
    det_boxes, det_scores = det_boxes[order], det_scores[order]

    iou = _iou_matrix(det_boxes, gt_boxes)
    ioa = _ioa_matrix(det_boxes, ignore_boxes)

    gt_taken = np.zeros(len(gt_boxes), dtype=bool)
    labels = np.zeros(len(det_boxes), dtype=np.int8)

    for i in range(len(det_boxes)):
        best_gt, best_iou = -1, iou_thr
        for j in range(len(gt_boxes)):
            if gt_taken[j] or iou[i, j] < best_iou:
                continue
            best_gt, best_iou = j, iou[i, j]

        if best_gt >= 0:
            gt_taken[best_gt] = True
            labels[i] = 1
        elif len(ignore_boxes) and ioa[i].max() >= ioa_thr:
            labels[i] = -1
        else:
            labels[i] = 0

    return det_scores, labels


def evaluate_detections(predictions, ground_truth, iou_thr=0.5, ioa_thr=0.5):
    """Hitung MR^-2 dan AP@0.5 atas seluruh dataset.

    `predictions` berbentuk {image_id: (boxes_xyxy ndarray, scores ndarray)}.
    Hanya citra yang ada di `ground_truth` yang dinilai.
    """
    all_scores, all_labels = [], []
    n_gt = 0
    n_images = 0

    for image_id, gt in ground_truth.items():
        if image_id not in predictions:
            continue

        n_images += 1
        n_gt += len(gt["boxes"])

        boxes, scores = predictions[image_id]
        if len(boxes) == 0:
            continue

        s, lab = _match_image(
            np.asarray(boxes, dtype=np.float64).reshape(-1, 4),
            np.asarray(scores, dtype=np.float64).reshape(-1),
            gt["boxes"],
            gt["ignore"],
            iou_thr,
            ioa_thr,
        )
        all_scores.append(s)
        all_labels.append(lab)

    if not all_scores or n_gt == 0:
        return {"mr2": 1.0, "ap50": 0.0, "recall_max": 0.0, "n_gt": n_gt, "n_images": n_images}

    scores = np.concatenate(all_scores)
    labels = np.concatenate(all_labels)

    # Buang deteksi yang jatuh di region ignore sebelum akumulasi.
    keep = labels >= 0
    scores, labels = scores[keep], labels[keep]

    order = np.argsort(-scores)
    labels = labels[order]

    tp = np.cumsum(labels == 1)
    fp = np.cumsum(labels == 0)

    recall = tp / n_gt
    precision = tp / np.maximum(tp + fp, 1e-9)
    miss_rate = 1.0 - recall
    fppi = fp / n_images

    # MR^-2: rata-rata logaritmik miss rate pada sembilan titik FPPI acuan.
    sampled = []
    for ref in FPPI_REFERENCE_POINTS:
        eligible = np.where(fppi <= ref)[0]
        sampled.append(miss_rate[eligible[-1]] if len(eligible) else 1.0)
    mr2 = float(np.exp(np.mean(np.log(np.maximum(sampled, 1e-9)))))

    # AP@0.5 dengan interpolasi presisi maksimum ke kanan (konvensi VOC/COCO).
    mrec = np.concatenate([[0.0], recall, [recall[-1]]])
    mpre = np.concatenate([[1.0], precision, [0.0]])
    mpre = np.maximum.accumulate(mpre[::-1])[::-1]
    ap50 = float(np.sum(np.diff(mrec) * mpre[1:]))

    return {
        "mr2": mr2,
        "ap50": ap50,
        "recall_max": float(recall[-1]),
        "n_gt": int(n_gt),
        "n_images": int(n_images),
    }
