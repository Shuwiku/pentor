from PIL import Image


def encrypt(text, font_symbols, font_symbols_images, symbols_in_row, delete_bad_symbols=False):
    text = text.replace('\n', ' ')
    if delete_bad_symbols:
        correct_text = ''
        for i in text:
            if i in font_symbols:
                correct_text += i
    else:
        correct_text = text
    lines = len(text) // symbols_in_row
    if symbols_in_row % 10 == 0:
        lines += 1
    image = Image.new(mode='RGB', size=(symbols_in_row * 11, lines * 11))
    x, y = 0, 0
    for i in correct_text:
        if i not in font_symbols:
            raise Exception(f'Symbol "{i}" not in font symbols!')
        i_image = font_symbols_images[font_symbols.index(i)]
        image.paste(i_image, (x, y))
        x += 11
        if x // 11 == symbols_in_row:
            x, y = 0, y + 11
    image.save('pentor.png')
