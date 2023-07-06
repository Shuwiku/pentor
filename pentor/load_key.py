import json
import os
import shutil
import zipfile

from PIL import Image, ImageChops

import config
from .load_image import load_image


def load_key(key_path):
    if not key_path:
        raise Exception('Key path is None.')
    _reset_temp_folder()
    with zipfile.ZipFile(key_path, mode='r') as f:
        f.extractall(config.TEMP_FOLDER)
    key_data_file = os.path.join(config.TEMP_FOLDER, config.KEY_DATA_FILE)
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


def _check_key_type_1(key_data):
    font_symbols = key_data.get('font-symbols')
    font_image = key_data.get('font-image')
    if font_symbols is None:
        raise Exception('Font symbols is None')
    font_image = os.path.join(config.TEMP_FOLDER, font_image)
    if font_image is None or not os.path.isfile(font_image):
        raise Exception('Font image is None')
    font_symbols_images = load_image(image_path=font_image)
    if len(font_symbols) != len(font_symbols_images):
        print(len(font_symbols), len(font_symbols_images))
        raise Exception('The number of characters must match the number of cropped character images.')
    return font_symbols, font_symbols_images


def _reset_temp_folder():
    if os.path.isdir(config.TEMP_FOLDER):
        shutil.rmtree(config.TEMP_FOLDER, 
                      ignore_errors=True,
                      onerror=None)
    os.mkdir(config.TEMP_FOLDER)
