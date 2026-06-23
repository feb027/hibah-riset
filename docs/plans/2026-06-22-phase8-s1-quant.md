"""Phase 8 — S1 Quantitative Evaluation (T1).

Latar belakang: Smoke test Tier 1 lulus (pipeline berjalan), tetapi hasil
deteksi per frame tidak cukup untuk klaim superiority. Phase 8 fokus pada
pengukuran mAP menggunakan dataset berlabel (ground truth).

Skenario:
1. S1-quant-inria: Baseline cepat (INRIA dataset, 614 images).
2. S1-quant-crowdhuman: Canonical crowd benchmark (CrowdHuman dataset, 15K images).

Tujuan: Membuktikan secara kuantitatif detector mana yang paling cocok
untuk crowd detection (occlusion, density) sebelum lanjut ke Tier 2 (Tracking).

Acceptance criteria:
- mAP dihitung menggunakan pycocotools.
- Hasil mAP dicatat untuk minimal 3 detector variants (S, N, M tiers).
- Hasil divalidasi terhadap ground truth, bukan sekadar count per frame.
- Reviewer pass menulis `docs/reviews/review-s1-quant.md`.
"""
# (No logic here, just a plan file)
