import os
import json
import zipfile
import shutil
from PIL import Image
from PyQt5.QtWidgets import QWidget, QFileDialog
from main_form import Ui_Form


class MainForm(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())
        self._key_path = None
        self._image_path = None
        self._enc = True
        self._set_buttons()
        self._set_radio_buttons()

    def _set_buttons(self):
        self._button_get_key_path.clicked.connect(self._get_key_path)
        self._button_get_image_path.clicked.connect(self._get_image_path)
        self._button_exit.clicked.connect(lambda: self.close())
        self._button_start.clicked.connect(self._start_app)

    def _set_radio_buttons(self):
        self._radio_button_dec.clicked.connect(self._change_mode(False))
        self._radio_button_enc.clicked.connect(self._change_mode(True))

    def _get_key_path(self):
        path = QFileDialog.getOpenFileName(self, 'Выбрать файл ключа', '', '(*.zip);;(*.7z)')[0]
        if not path:
            return
        self._key_path = path
        self._line_edit_key_path.setText(path)

    def _get_image_path(self):
        path = QFileDialog.getOpenFileName(self, 'Выбрать изображение с текстом', '', '(*.png)')[0]
        if not path:
            return
        self._image_path = path
        self._line_image_path.setText(path)

    def _change_mode(self, _is_enc):
        
        def mode():
            print(_is_enc)
            self._enc = _is_enc

        return mode

    def _start_app(self):
        if self._enc:
            self._encrypt()
        else:
            self._decrypt()

    def _encrypt(self):
        if os.path.isdir('temp'):
            shutil.rmtree('temp', ignore_errors=False, onerror=None)
        os.mkdir('temp')
        with zipfile.ZipFile(self._key_path, mode='r') as f:
            f.extractall('temp')
        font_data = 'data.json'
        cpath = os.getcwd()
        tpath = os.path.join(cpath, 'temp')
        fpath = os.path.join(tpath, font_data)
        with open(fpath, mode='r') as f:
            data = json.load(f)
        font_file = os.path.join(tpath, data.get('key_font_image'))
        symb = data.get('symbols')
        image = Image.open(font_file)
        w, h = image.size
        if w % 9 != 0 or h % 9 != 0:
            return
        images = []
        x, y = 0, 0
        for i in range(h // 9):
            for j in range(w // 9):
                croped = image.crop((x, y, x + 9, y + 9))
                images.append(croped)
                x += 9
            y += 9
            x = 0
        text = self._plain_text_edit_text.toPlainText()
        text = text.upper()
        s_in_row = int(self._spin_box_max_symb_in_row.value())
        lines = len(text) // s_in_row + 1
        image = Image.new(mode='RGB', size=(s_in_row * 9, lines * 9))
        x, y = 0, 0
        for i in text:
            print(x, y)
            _index = symb.index(i)
            img = images[_index]
            image.paste(img, (x, y))
            x += 9
            if x // 9 >= s_in_row:
                x = 0
                y += 9
        image.save('RES.jpg')
