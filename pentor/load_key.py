import json
import os
import shutil
import zipfile

from PIL import Image, ImageChops

from . import config


def load_key(key_path):
    if not key_path:  # Ошибка, если не указан путь к ключу
        raise Exception('Key path is None.')
    _reset_temp_folder()
    # Распаковываем ключ в папку
    with zipfile.ZipFile(key_path, mode='r') as f:
        f.extractall(config.TEMP_FOLDER)
    key_data_file = os.path.join(config.TEMP_FOLDER, config.KEY_DATA_FILE)
    # Если нет файла с данными ключа
    if not os.path.isfile(key_data_file):
        raise Exception('There is no key data file.')
    func = {
        1: _check_key_type_1
    }
    with open(key_data_file, mode='r') as f:
        key_data = json.load(f)
        key_type = key_data.get('key-type')
        if key_type is None or key_type not in list(func.keys()):
            raise Exception('Key type None or unknown')
        font_symbols, font_symbols_images = func.get(key_type)(key_data=key_data)
    return font_symbols, font_symbols_images


def _reset_temp_folder():
    # Удаляем папку с временными файлами
    if os.path.isdir(config.TEMP_FOLDER):
        shutil.rmtree(config.TEMP_FOLDER, 
                      ignore_errors=True,
                      onerror=None)
    # Создаём папку с временными файлами
    os.mkdir(config.TEMP_FOLDER)


def _check_key_type_1(key_data):
    font_symbols = key_data.get('font-symbols')
    font_image = key_data.get('font-image')
    if font_symbols is None:
        raise Exception('Font symbols is None')
    font_image = os.path.join(config.TEMP_FOLDER, font_image)
    if font_image is None or not os.path.isfile(font_image):
        raise Exception('Font image is None')
    font_symbols_images = _crop_font_image(font_image=font_image)
    if len(font_symbols) != len(font_symbols_images):
        print(len(font_symbols), len(font_symbols_images))
        raise Exception('The number of characters must match the number of cropped character images.')
    return font_symbols, font_symbols_images


def _crop_font_image(font_image):
    image = Image.open(font_image)
    width, height = image.size
    if width % 11 != 0 or height % 11 != 0:
        raise Exception('Font image height or width is not a multiple of 11')
    font_symbols_images = []
    x, y = 0, 0
    for i in range(height // 11):
        for j in range(width // 11):
            crop_coords = (x, y, x + 11, y + 11)
            symbol_image = image.crop(crop_coords)
            if _check_symbol_image(symbol_image=symbol_image):
                break
            font_symbols_images.append(symbol_image)
            x += 11
        x, y = 0, y + 11
    return font_symbols_images


def _check_symbol_image(symbol_image):
    empty_symbol = Image.new(mode='RGB', size=(11, 11), color=(96,96,112))
    empty_symbol.paste(im=Image.new(mode='RGB', size=(9, 9), color=(0, 0, 0)),
                       box=(1, 1))
    diff = ImageChops.difference(image1=symbol_image.convert('RGB'), 
                                 image2=empty_symbol.convert('RGB'))
    if not diff.getbbox():
        return True
    return False
