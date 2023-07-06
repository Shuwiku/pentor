def encrypt(key_path: str,
            text: str,
            copy_image_scale: int = None,
            delete_bad_symbols: bool = False,
            symbols_in_row: int = 1,
            text_case: str = None):
    """Функция для 'шифрования' текста в изображение по
    пользовательсому ключу."""
