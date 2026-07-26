"""Helper pengukuran latensi yang dipakai bersama oleh script benchmark.

Dipisahkan ke modul sendiri agar protokol pengukurannya identik di seluruh
eksperimen. Kalau tiap script memakai jumlah pemanasan atau cara agregasi yang
berbeda, angkanya tidak bisa disandingkan - padahal justru menyandingkan angka
antar perangkat itulah tujuan Skenario A dan D.
"""
from __future__ import annotations

import statistics

__all__ = ["warmup", "percentile", "summarize"]


def warmup(model, image_paths, rounds, **predict_kwargs):
    """Panaskan model sampai kondisi tunak sebelum pengukuran dimulai.

    Pemanasan menyapu SELURUH gambar uji, bukan satu gambar saja: ukuran gambar
    bervariasi, dan tiap ukuran baru memicu alokasi buffer yang biayanya akan
    tercatat sebagai latensi kalau belum dihangatkan. Pada GPU, putaran yang
    cukup panjang juga diperlukan agar clock naik ke frekuensi kerjanya.
    """
    for _ in range(rounds):
        for img_path in image_paths:
            model(img_path, verbose=False, **predict_kwargs)


def percentile(values, q):
    """Persentil ke-q dengan interpolasi linear; aman untuk sampel kecil."""
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * q
    low = int(pos)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (pos - low)


def summarize(values):
    """Statistik latensi: median dan p95 sebagai angka utama, mean/sd pendamping.

    Distribusi latensi menjulur ke kanan - beberapa iterasi lambat menarik
    rata-rata naik tanpa mewakili perilaku biasa. Median lebih mewakili kondisi
    tunak, sedangkan p95 menggambarkan beban puncak, dan justru p95 inilah yang
    relevan untuk sistem real-time.
    """
    return {
        "p50": statistics.median(values),
        "p95": percentile(values, 0.95),
        "mean": statistics.mean(values),
        "sd": statistics.stdev(values) if len(values) > 1 else 0.0,
    }
