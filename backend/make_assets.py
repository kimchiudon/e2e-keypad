from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ASSETS = Path("assets")
ASSETS.mkdir(exist_ok=True)

W, H = 200, 200

def make_img(text: str, filename: str):
    img = Image.new("RGBA", (W, H), (245, 245, 245, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        font = ImageFont.load_default()


    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (W - tw) // 2
    y = (H - th) // 2

    draw.rectangle([10, 10, W - 10, H - 10], outline=(180, 180, 180, 255), width=4)
    draw.text((x, y), text, fill=(50, 50, 50, 255), font=font)

    img.save(ASSETS / filename)

for i in range(10):
    make_img(str(i), f"{i}.png")


make_img("", "EMPTY.png")

print("assets generated in ./assets")
