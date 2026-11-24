from requests import get
from PIL import Image
from pathlib import Path
from io import BytesIO
from threading import Thread, Lock
from bars import DownloadBar
from sys import stderr

lock = Lock()


folder = Path("practice/datasets/data")
folder.mkdir(parents=True, exist_ok=True)

def download_image(url:str, filename:str, size=(256, 256), quality=85):
    """Downloads an image from your url to the folder you set\n
    WARNING: Works ONLY with jpg format

    Args:
        url (_type_): _description_
        filename (_type_): _description_
        size (tuple, optional): _description_. Defaults to (256, 256).
        quality (int, optional): _means quality of output image_. Defaults to 85.
    """
    
    response = get(url, timeout=15)
    response.raise_for_status()

    with Image.open(BytesIO(response.content)) as image:
        image = image.convert("RGB")

        # Изменяем размер без обрезки и искажения пропорций
        image.thumbnail(size, Image.Resampling.LANCZOS)

        # Сохраняем в WebP со сжатием
        image.save(filename, format="WEBP", quality=quality)

def download_worker(url, filename, bar):
    try:
        download_image(url, filename)

    except Exception as error:
        with lock:
            bar.failed += 1

    finally:
        with lock:
            bar.next()
            bar.file.flush()

def download_worker(url, filename, bar):
    failed = False

    try:
        download_image(url, filename)

    except Exception:
        failed = True

    finally:
        with lock:
            bar.failed += int(failed)
            bar.next()
            bar.file.flush()


# TODO: Написать код, который в папку data скачает всех котов (1000 изображений)
# TODO: Написать код, который в папку data скачает всех собак (1000 изображений)
# TODO: С помощью библиотеки httpx реализовать асинхронные скачивания датасетов
# TODO: Написать код для модели Pytorch (без Convolution и Pooling и Vision функций)  
# TODO: Создать метрики для модели
# TODO: Научиться визуализировать прогресс обучения, давать оценки, стоимость, дедлайны и качество итоговое


MAX_THREADS = 50
threads:list[Thread] = []

with DownloadBar("Downloading", max=1000, file=stderr) as bar:
    for page in range(1, 101):
        data = get(
            f"https://api.thecatapi.com/v1/images/search?limit=10&page={page}",
            timeout=15
        ).json()

        for i in range(len(data)):
            url: str = data[i]["url"]
            
            if url.endswith(".jpg"):
                filename = folder / f"cat_{page}_{i}.webp"

                thread = Thread(
                    target=download_worker,
                    args=(url, filename, bar)
                )

                thread.start()
                threads.append(thread)

                if len(threads) >= MAX_THREADS:

                    for t in threads:
                        t.join()
                    threads.clear()

    # Ожидаем завершения оставшихся потоков
    for thread in threads:
        thread.join()

print("Загрузка завершена")