"""LightTrack-ReID-inspired (Phase 3) — FLTC crop cache + APS pair sampling.

FLTC (Frame-Level Temporal Cache): cache per-frame kumpulan crop 224x224 uint8
(dan bbox GT + id) dari semua deteksi frame tsb — BUKAN frame utuh half-res.
Mengurangi I/O dari ~100rb pair-tensor menjadi ~2rb frame-tensor. uint8 =
4x lebih hemat dari float32. LRU cap frames caplah.

APS (Active Pair Sampling): per frame, bangun sampel triplet
    (anchor_crop, pos_crop, neg_crop)
- pos  = crop yang SAMA id tetapi dari frame beda (id sama, frame beda)
- neg  = crop id BEDA dalam frame yang sama (frame sama, id beda)
Maks `max_pairs` triplet/frame, seimbang. Kedua loss (triplet + BCE) diturunkan
dari satu triplet: triplet memakai (a,p,n); BCE memakai (a,p)->1 dan (a,n)->0.

Index id->frames (FLTC): kandidat positif dicari lewat index GT — TANPA decode
gambar — persis APS paper (maks 50 pasangan/frame, sampling dari label).
Frame yang benar-benar dipakai baru diterjemahkan via LRU cache.

py3.8-friendly (tanpa list[int]/X | None). TORCH-ONLY di jalur training.
"""
import os
from collections import defaultdict, OrderedDict

import numpy as np


CROP = 224


class FLTCCache:
    """Cache crop per frame (LRU) dari satu sekuens MOT.

    `.frame(t)` mengembalikan list dict: {id:int, box:(x,y,w,h), crop:uint8 (CROP,CROP,3)}.
    `.frames_of(i)` mengembalikan sorted frame list dari GT index (nol I/O gambar).
    """

    def __init__(self, seq_dir, cap=2048):
        self.seq_dir = seq_dir
        self.cap = cap
        self.img_dir = os.path.join(seq_dir, "img1")
        self._gt = self._load_gt()
        self._frames = OrderedDict()  # LRU: frame -> list dict
        self._by_frame = defaultdict(list)
        self._by_id = defaultdict(list)  # index id -> sorted frame list
        self._size = None
        for row in self._gt:
            fr = int(row[0])
            self._by_frame[fr].append(row)
            self._by_id[int(row[1])].append(fr)
        for k in self._by_id:
            self._by_id[k] = sorted(set(self._by_id[k]))

    def _load_gt(self):
        rows = []
        gt_path = os.path.join(self.seq_dir, "gt", "gt.txt")
        with open(gt_path) as fh:
            for line in fh:
                p = line.strip().split(",")
                if len(p) < 9:
                    continue  # baris tidak lengkap / kosong
                fr = int(float(p[0]))
                idx = int(float(p[1]))
                x, y, w, h = (float(p[i]) for i in (2, 3, 4, 5))
                conf, cls_, vis = float(p[6]), float(p[7]), float(p[8])
                if not (conf == 1 and cls_ == 1 and vis > 0):
                    continue  # hanya deteksi pedestrian valid (sama dgn verify script)
                rows.append((fr, idx, x, y, w, h))
        return rows

    def frames(self):
        return sorted(self._by_frame.keys())

    def frames_of(self, track_id):
        """Sorted frame list di mana track_id muncul — dari GT, TANPA decode gambar.

        Inti FLTC+APS: cari kandidat positif lewat index, bukan decode.
        """
        return self._by_id.get(track_id, ())

    def frame_size(self):
        """(H, W) frame utuh (di-cache). Dipakai clamp box utk IoU dgn frame dimensi asli."""
        import cv2
        if self._size is None:
            p = os.path.join(self.img_dir, f"{self.frames()[0]:06d}.jpg")
            img = cv2.imread(p, cv2.IMREAD_COLOR)
            if img is None:
                raise FileNotFoundError(p)
            self._size = img.shape[:2]
        return self._size

    def _read_crop(self, img_bgr, x, y, w, h):
        """Crop (224,224,3) ONE box dari frame utuh (img_bgr) yang sudah dibaca sekali."""
        import cv2
        hh, ww = img_bgr.shape[:2]
        x = max(0, int(round(x))); y = max(0, int(round(y)))
        x2 = min(ww, x + max(1, int(round(w))))
        y2 = min(hh, y + max(1, int(round(h))))
        c = img_bgr[y:y2, x:x2]
        if c.size == 0:
            return None
        return cv2.resize(c, (CROP, CROP), interpolation=cv2.INTER_AREA)

    def frame(self, t):
        """list deteksi frame t dengan crop (LRU-dicache).

        Baca frame JPEG SEKALI per panggilan, lalu crop SEMUA deteksi dari buffer
        yg sama (awalnya: imread per deteksi -> 20-50x decode JPEG per frame).
        """
        if t in self._frames:
            self._frames.move_to_end(t)
            return self._frames[t]
        import cv2
        p = os.path.join(self.img_dir, f"{t:06d}.jpg")
        bgr = cv2.imread(p, cv2.IMREAD_COLOR)
        items = []
        if bgr is not None:
            for box in self._by_frame.get(t, ()):
                crop = self._read_crop(bgr, box[2], box[3], box[4], box[5])
                if crop is None:
                    continue
                items.append(dict(id=box[1], box=(box[2], box[3], box[4], box[5]), crop=crop))
        self._frames[t] = items
        self._frames.move_to_end(t)
        while len(self._frames) > self.cap:
            self._frames.popitem(last=False)
        return items


class APSSampler:
    """APS: triplet (anchor,pos,neg) per frame, max max_pairs/frame.

    Dipanggil tiap epoch dengan urutan frame per-sekuens (bukan shuffle global,
    supaya LRU cache frame bertahan). Cari positif dari index GT — TANPA decode
    frame kandidat. Frame terpilih didecode sekali via LRU.
    """

    def __init__(self, window=15, max_pairs=50, seed=0):
        self.window = window   # jendela frame utk cari pos (id sama, frame ~dekat)
        self.max_pairs = max_pairs
        self.rng = np.random.RandomState(seed)

    def sample(self, cache, t):
        """List maks max_pairs triplet (anchor,pos,neg) + box untuk frame t.

        tiap item: dict(a=(crop,bx), p=(crop,bx), n=(crop,bx)).
        """
        dets = cache.frame(t)
        if len(dets) < 2:
            return []
        ids = {d["id"] for d in dets}
        # kandidat: semua frame dalam window yang memuat id manapun di frame t
        cand = []
        for i in ids:
            for tt in cache.frames_of(i):
                if tt != t and abs(tt - t) <= self.window and tt not in cand:
                    cand.append(tt)
        if not cand:
            return []
        self.rng.shuffle(cand)
        out = []
        pos_cache = {}
        for d in dets:
            if len(out) >= self.max_pairs:
                break
            # positif: frame kandidat yang memuat id yang sama (id sama)
            fr_id = set(cache.frames_of(d["id"]))
            pos = next((tt for tt in cand if tt in fr_id), None)
            if pos is None:
                continue
            if pos not in pos_cache:
                pos_cache[pos] = cache.frame(pos)
            pos_frm = pos_cache[pos]
            pos_d = next((r for r in pos_frm if r["id"] == d["id"]), None)
            if pos_d is None:
                continue
            # negatif: id beda dalam frame yang sama
            negs = [r for r in dets if r["id"] != d["id"]]
            if not negs:
                continue
            neg = negs[self.rng.randint(len(negs))]
            out.append(dict(a=(d["crop"], d["box"]), p=(pos_d["crop"], pos_d["box"]),
                            n=(neg["crop"], neg["box"])))
        return out


def _demo():
    # self-check sintetis tanpa data MOT: buat cache fake di memori.
    class FakeCache:
        def __init__(self):
            self._fr = {1: [dict(id=1, box=(1, 1, 8, 8), crop=np.full((CROP, CROP, 3), 128, np.uint8)),
                            dict(id=2, box=(50, 1, 8, 8), crop=np.full((CROP, CROP, 3), 200, np.uint8))],
                        2: [dict(id=1, box=(1, 2, 8, 8), crop=np.full((CROP, CROP, 3), 128, np.uint8)),
                            dict(id=3, box=(80, 1, 8, 8), crop=np.full((CROP, CROP, 3), 200, np.uint8))]}
        def frame(self, t):
            return self._fr[t]
        def frames_of(self, i):
            return [t for t, ds in self._fr.items() if any(d["id"] == i for d in ds)]
    s = APSSampler(window=5, max_pairs=10, seed=1)
    out = s.sample(FakeCache(), 1)
    assert out, "APS kosong di frame penuh"
    for tr in out:
        a, p, n = tr["a"][0], tr["p"][0], tr["n"][0]
        assert (a == p).all()
        assert not (a == n).all()
        assert len(tr["a"][1]) == 4 and len(tr["p"][1]) == 4
    print("demo OK", {"triplet_cnt": len(out),
                      "sample_shapes": [tuple(tr["a"][0].shape), tuple(tr["p"][0].shape),
                                        tuple(tr["n"][0].shape)]})


if __name__ == "__main__":
    _demo()