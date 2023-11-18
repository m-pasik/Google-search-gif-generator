import sys
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

google = Image.open("google.png")
google = google.convert("RGBA")

font = ImageFont.truetype("ARIAL.ttf", 16)

if len(sys.argv) < 4:
    n = 0
    txt = " ".join(list(sys.stdin))
    args = [sys.argv[1], sys.argv[2]]
else:
    txt = sys.argv[1]
    args = [sys.argv[2], sys.argv[3]]

txt = txt.replace("\n", "").replace("\r", "")

length = len(txt)
max_count_len = len(str(length))*2+1
bar_len = 50

def printProgress(x):
    count = str(x) + "/" + str(length)
    progress = int(bar_len * (x / length))
    sys.stdout.write("\r")
    sys.stdout.write("Generating frames	%s [%s]" %
                        (" " * (max_count_len - len(count)) + count,
                        ("#" * progress) + ("-" * (bar_len - progress))))
    sys.stdout.flush()

frames = []

chars = 0

for i in range(length + 1):
    img = Image.new(mode='RGBA', size=(441,20), color=(255,255,255,255))
    draw = ImageDraw.Draw(img)
    pos = font.getlength(txt[:i])
    x = 1
    if pos > 440:
        while font.getlength(txt[chars+1:i]) > 440:
            chars += 1
        x = 440 - font.getlength(txt[chars:i])
        pos = 440
    draw.text((x, 0), txt[chars:i], font=font, fill=(21,21,21,255))
    draw.line([(pos, 1), (pos, 17)], fill=(21,21,21,255), width=1)
    out = google.copy()
    out.paste(img, (64,147))
    frames.append(out)
    printProgress(i)

sys.stdout.write("\n")

frames[0].save(args[1], save_all=True, append_images=frames[1:], duration=int(args[0]))
