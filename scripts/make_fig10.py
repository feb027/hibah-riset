"""Gambar 4 versi 2x3: 4 tracker + GT + crop zoom area padat - .venv-s2/bin/python."""
from PIL import Image, ImageDraw, ImageFont

base = 'experiments/journal_figs'
panels = [
    ('frame_ocsort.png', 'a) OC-SORT'),
    ('frame_deepocsort.png', 'b) Deep-OC-SORT'),
    ('frame_diffmot.png', 'c) DiffMOT'),
    ('frame_lighttrack.png', 'd) LightTrack'),
    ('frame_gt.png', 'e) Ground Truth'),
]
imgs = [Image.open(f'{base}/{f}') for f, _ in panels]
w, h = imgs[0].size
# crop area tengah (kerumunan padat) untuk baris bawah: kotak tengah 55%x55%
cw, ch = int(w * 0.55), int(h * 0.55)
cx, cy = (w - cw) // 2, (h - ch) // 2
zooms = [im.crop((cx, cy, cx + cw, cy + ch)) for im in imgs]
# upscale crop ke lebar kolom biar 2 baris sama lebar
zooms = [z.resize((w, int(ch * w / cw))) for z in zooms]
zh = zooms[0].height

label_h = 46
gap = 14
W = w * 3 + gap * 2
H = (label_h + h) + gap + (label_h + zh)
canvas = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
except OSError:
    font = ImageFont.load_default()

def paste_labeled(idx, x, y):
    lab = panels[idx][1]
    canvas.paste(imgs[idx], (x, y + label_h))
    bb = d.textbbox((0, 0), lab, font=font)
    d.text((x + (w - (bb[2] - bb[0])) // 2, y + 8), lab, fill='black', font=font)

def paste_zoom(idx, x, y):
    lab = panels[idx][1].replace(')', ' - zoom)')
    canvas.paste(zooms[idx], (x, y + label_h))
    bb = d.textbbox((0, 0), lab, font=font)
    d.text((x + (w - (bb[2] - bb[0])) // 2, y + 8), lab, fill='black', font=font)

# baris 1: OC-SORT, Deep-OC-SORT, DiffMOT
for i in range(3):
    paste_labeled(i, i * (w + gap), 0)
# baris 2: LightTrack, GT (2 kolom terakhir digabung untuk zoom GT supaya seimbang)
paste_labeled(3, 0, label_h + h + gap)
paste_labeled(4, w + gap, label_h + h + gap)
canvas.save(f'{base}/fig10_demo_qualitative.png')
print('OK', canvas.size)
