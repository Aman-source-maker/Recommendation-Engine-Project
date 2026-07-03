from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ASSETS_DIR = Path(__file__).resolve().parent / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

MOVIES = [
    ("toy-story-1995.png", "TOY\nSTORY", ("#0b67a3", "#e8b923")),
    ("jumanji-1995.png", "JUMANJI", ("#143c2c", "#b8843b")),
    ("heat-1995.png", "HEAT", ("#11151c", "#c23b22")),
    ("goldeneye-1995.png", "GOLDENEYE", ("#111111", "#d7aa33")),
    ("twelve-monkeys-1995.png", "TWELVE\nMONKEYS", ("#302642", "#7aa35a")),
    ("seven-1995.png", "SE7EN", ("#171717", "#8f1f1f")),
    ("usual-suspects-1995.png", "THE USUAL\nSUSPECTS", ("#1b2838", "#d0d0c8")),
    ("braveheart-1995.png", "BRAVEHEART", ("#18334a", "#c8d6e5")),
    ("star-wars-1977.png", "STAR\nWARS", ("#050505", "#f1c232")),
    ("pulp-fiction-1994.png", "PULP\nFICTION", ("#1c1b16", "#d9b43b")),
]


def load_font(size):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def make_gradient(width, height, start_hex, end_hex):
    start = tuple(int(start_hex[i:i + 2], 16) for i in (1, 3, 5))
    end = tuple(int(end_hex[i:i + 2], 16) for i in (1, 3, 5))
    image = Image.new("RGB", (width, height), start)
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            ratio = (x / width * 0.65) + (y / height * 0.35)
            color = tuple(int(start[channel] * (1 - ratio) + end[channel] * ratio) for channel in range(3))
            pixels[x, y] = color

    return image


def draw_poster(filename, title, colors):
    width, height = 1280, 720
    image = make_gradient(width, height, colors[0], colors[1])
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for i in range(12):
        x0 = -120 + i * 140
        draw.rectangle((x0, 0, x0 + 56, height), fill=(255, 255, 255, 14))

    draw.rectangle((0, int(height * 0.56), width, height), fill=(0, 0, 0, 122))
    draw.ellipse((width - 430, -180, width + 210, 460), fill=(255, 255, 255, 24))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=1.1))
    image = Image.alpha_composite(image.convert("RGBA"), overlay)

    draw = ImageDraw.Draw(image)
    font = load_font(106 if len(title) < 11 else 84)
    small_font = load_font(30)

    lines = title.splitlines()
    line_heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
    total_height = sum(line_heights) + (len(lines) - 1) * 8
    y = height - total_height - 105

    for line in lines:
        draw.text((62, y), line, font=font, fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 150))
        y += draw.textbbox((0, 0), line, font=font)[3] + 8

    draw.text((66, height - 54), "MOVIELENS PREVIEW", font=small_font, fill=(230, 230, 230, 220))
    image.convert("RGB").save(ASSETS_DIR / filename, quality=92)


for movie in MOVIES:
    draw_poster(*movie)

print(f"Generated {len(MOVIES)} thumbnails in {ASSETS_DIR}")
