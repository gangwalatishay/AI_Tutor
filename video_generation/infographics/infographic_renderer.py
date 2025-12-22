from PIL import Image, ImageDraw, ImageFont
import os


def render_infographic(scene, output_path, size=(1280, 720)):
    img = Image.new("RGB", size, "#0f172a")
    draw = ImageDraw.Draw(img)

    title = scene.get("title", "")
    stats = scene.get("stats", [])

    # Fallback font
    font_title = ImageFont.load_default()
    font_stat = ImageFont.load_default()

    draw.text((50, 40), title, fill="white", font=font_title)

    y = 150
    for stat in stats:
        draw.text((100, y), f"{stat['value']}", fill="#38bdf8", font=font_stat)
        draw.text((300, y), stat["label"], fill="white", font=font_stat)
        y += 80

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)

    return output_path
