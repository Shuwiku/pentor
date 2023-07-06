from PIL import Image

from .load_key import load_key


def encrypt(key_path, text, copy_image_scale=None, delete_bad_symbols=False,
            symbols_in_row=1, text_case=None):
    font_symbols, font_symbols_images = load_key(key_path=key_path)
    text = _edit_text(text=text, delete_bad_symbols=delete_bad_symbols,
                      font_symbols=font_symbols, text_case=text_case)
    lines = len(text) // symbols_in_row
    if len(text) % symbols_in_row != 0:
        lines += 1
    image = Image.new(mode='RGB', size=(symbols_in_row * 11, lines * 11))
    pos_x, pos_y = 0, 0
    for symb in text:
        if symb not in font_symbols:
            raise Exception(f'Символ "{symb}" не находится в списке символов ключа!')
        if pos_x // 11 == symbols_in_row:
            pos_x, pos_y = 0, pos_y + 11
        symb_image = font_symbols_images[font_symbols.index(symb)]
        image.paste(symb_image, (pos_x, pos_y))
        pos_x += 11
    image.save('pentor.png')


def _edit_text(text, delete_bad_symbols, font_symbols, text_case):
    text = text.replace('\n', ' ')
    if text_case is not None:
        if text_case == 'lower':
            text = text.lower()
        elif text_case == 'upper':
            text = text.upper()
    if delete_bad_symbols:
        cor_symbols = [i for i in text if i in font_symbols]
        text = ''.join(cor_symbols)
    return text
