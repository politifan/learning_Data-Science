from requests import get
from PIL import Image
from pathlib import Path
from io import BytesIO

folder = Path("practice/datasets/data")
folder.mkdir(exist_ok=True)

def download_image(url, filename, size=(256, 256), quality=85):

    response = get(url, timeout=15)
    response.raise_for_status()

    with Image.open(BytesIO(response.content)) as image:
        image = image.convert("RGB")

        # Изменяем размер без обрезки и искажения пропорций
        image.thumbnail(size, Image.Resampling.LANCZOS)

        # Сохраняем в WebP со сжатием
        image.save(filename, format="WEBP", quality=quality)

data = get("https://api.thecatapi.com/v1/images/search?limit=2&page=1").json()

# TODO: Написать код, который в папку data скачает всех котов (1000 изображений)
# TODO: Написать код, который в папку data скачает всех собак (1000 изображений)
# TODO: С помощью библиотеки httpx реализовать асинхронные скачивания датасетов
# TODO: Написать код для модели Pytorch (без Convolution и Pooling и Vision функций)  
# TODO: Создать метрики для модели
# TODO: Научиться визуализировать прогресс обучения, давать оценки, стоимость, дедлайны и качество итоговое




for i in range(len(data)):

    url:str = data[i]["url"]
    if url.endswith(".gif"): continue

    download_image()