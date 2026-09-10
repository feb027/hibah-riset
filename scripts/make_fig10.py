"""Gabung 3 frame demo jadi satu figur side-by-side (OC-SORT | DiffMOT | GT) - .venv-s2/bin/python."""
from PIL import Image, ImageDraw, ImageFont

base = 'experiments/journal_figs'
names = [('fig10a_ocsort.png', 'a) OC-SORT'), ('fig10b_diffmot.png', 'b) DiffMOT'), ('fig10c_gt.png', 'c) Ground Truth')]
imgs = [Image.open(f'{base}/{f}') for f, _ in names]
w, h = imgs[0].size
label_h = 44
canvas = Image.new('RGB', (w * 3 + 20 * 2, h + label_h), 'white')
d = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
except OSError:
    font = ImageFont.load_default()
x = 0
for (f, lab), im in zip(names, imgs):
    canvas.paste(im, (x, label_h))
    bbox = d.textbbox((0, 0), lab, font=font)
    d.text((x + (w - (bbox[2] - bbox[0])) // 2, 8), lab, fill='black', font=font)
    x += w + 20
canvas.save(f'{base}/fig10_demo_qualitative.png')
print('OK', canvas.size)
