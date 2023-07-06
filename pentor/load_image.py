from PIL import Image, ImageChops


def load_image(image_path):
    image = Image.open(image_path)
    width, height = image.size
    if width % 11 != 0 or height % 11 != 0:
        raise Exception('Image height or width is not a multiple of 11')
    image_symbols = []
    x, y = 0, 0
    for i in range(height // 11):
        for j in range(width // 11):
            crop_coords = (x, y, x + 11, y + 11)
            symbol_image = image.crop(crop_coords)
            if _check_symbol_image(symbol_image=symbol_image):
                break
            image_symbols.append(symbol_image)
            x += 11
        x, y = 0, y + 11
    return image_symbols


def _check_symbol_image(symbol_image):
    empty_symbol = Image.new(mode='RGB', size=(11, 11), color=(0, 0, 0))
    diff = ImageChops.difference(image1=symbol_image.convert('RGB'), 
                                 image2=empty_symbol.convert('RGB'))
    if not diff.getbbox():
        return True
    return False
