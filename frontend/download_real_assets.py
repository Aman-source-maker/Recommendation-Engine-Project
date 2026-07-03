from io import BytesIO
from pathlib import Path
from time import sleep
from urllib.request import Request, urlopen

from PIL import Image


ASSETS_DIR = Path(__file__).resolve().parent / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

POSTERS = {
    "toy-story-1995.png": "https://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",
    "jumanji-1995.png": "https://upload.wikimedia.org/wikipedia/en/b/b6/Jumanji_poster.jpg",
    "heat-1995.png": "https://upload.wikimedia.org/wikipedia/en/6/6c/Heatposter.jpg",
    "goldeneye-1995.png": "https://upload.wikimedia.org/wikipedia/en/2/24/GoldenEye_-_UK_cinema_poster.jpg",
    "twelve-monkeys-1995.png": "https://upload.wikimedia.org/wikipedia/en/c/cf/Twelve_monkeysmp.jpg",
    "seven-1995.png": "https://upload.wikimedia.org/wikipedia/en/6/68/Seven_%28movie%29_poster.jpg",
    "usual-suspects-1995.png": "https://upload.wikimedia.org/wikipedia/en/9/9c/Usual_suspects_ver1.jpg",
    "braveheart-1995.png": "https://upload.wikimedia.org/wikipedia/en/e/e1/Braveheart_film_poster.png",
    "star-wars-1977.png": "https://upload.wikimedia.org/wikipedia/en/8/87/StarWarsMoviePoster1977.jpg",
    "pulp-fiction-1994.png": "https://upload.wikimedia.org/wikipedia/en/3/3b/Pulp_Fiction_%281994%29_poster.jpg",
}

FORCE_REFRESH = {
    "twelve-monkeys-1995.png",
    "seven-1995.png",
    "usual-suspects-1995.png",
    "braveheart-1995.png",
    "star-wars-1977.png",
    "pulp-fiction-1994.png",
}


def download_image(url):
    request = Request(url, headers={"User-Agent": "MovieLensDemo/1.0"})
    with urlopen(request, timeout=30) as response:
        return Image.open(BytesIO(response.read())).convert("RGB")


def fit_to_poster(image, size=(640, 960)):
    image.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, (10, 10, 10))
    x = (size[0] - image.width) // 2
    y = (size[1] - image.height) // 2
    canvas.paste(image, (x, y))
    return canvas


for filename, url in POSTERS.items():
    output_path = ASSETS_DIR / filename
    if filename not in FORCE_REFRESH and output_path.exists() and output_path.stat().st_size > 20000:
        print(f"skipped {filename}")
        continue

    image = download_image(url)
    poster = fit_to_poster(image)
    poster.save(output_path, quality=92)
    print(f"saved {filename}")
    sleep(8)

print(f"Downloaded {len(POSTERS)} real poster thumbnails.")
