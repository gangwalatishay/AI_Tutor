from PIL import Image, ImageDraw, ImageFont
import os


def generate_image(prompt: str, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    img = Image.new("RGB", (1280, 720), color=(15, 15, 20))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("Arial.ttf", 32)
    except:
        font = ImageFont.load_default()

    draw.text((40, 300), prompt[:200], fill="white", font=font)
    img.save(output_path)

    return output_path
