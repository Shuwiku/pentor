from PIL import ImageChops

from .load_image import load_image
from .load_key import load_key


def decrypt(image_path, key_path):
    symbols_images = load_image(image_path=image_path)
    font_symbols, font_symbols_images = load_key(key_path=key_path)
    text = ''
    for i in symbols_images:
        for k, j in enumerate(font_symbols_images):
            diff = ImageChops.difference(image1=i.convert('RGB'),
                                         image2=j.convert('RGB'))
            if not diff.getbbox():
                text += font_symbols[k]
    with open('pentor.txt', mode='w') as f:
        f.write(text)
