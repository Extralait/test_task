import os

from PIL import Image

from Config.settings import MEDIA_ROOT


def add_watermark(image):
    watermark = Image.open(os.path.join(MEDIA_ROOT, "static/watermark.png"))
    image_path = str(image)
    image = Image.open(image)
    image.paste(watermark, (image.size[0] - watermark.size[0], image.size[1] - watermark.size[1]), watermark)
    image.save(os.path.join(MEDIA_ROOT, image_path))


