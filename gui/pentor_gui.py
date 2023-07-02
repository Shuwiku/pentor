import os
import shutil
import zipfile

from PyQt5.QtWidgets import QWidget, QFileDialog

import pentor
from .form import Ui_PentorForm


class PentorGUI(QWidget, Ui_PentorForm):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())

        self._font_symbols = None
        self._font_symbols_images = None
        
        self._setup_buttons()
        self._setup_radio_buttons()

    def _setup_buttons(self):
        self._button_about.clicked.connect(lambda: ...)
        self._button_load_image.clicked.connect(self._load_image)
        self._button_load_key.clicked.connect(self._load_key)
        self._button_start.clicked.connect(self._start)

    def _setup_radio_buttons(self):
        self._radio_button_encrypt.toggled.connect(self._change_mode)
        self._radio_button_encrypt.setChecked(True)
        self._change_mode()

    def _change_mode(self):
        if self._radio_button_encrypt.isChecked():
            self._line_edit_image_path.setDisabled(True)
            self._button_load_image.setDisabled(True)
            self._plain_text_edit_text.setDisabled(False)
            self._spin_box_symbols_in_row.setDisabled(False)
        else:
            self._plain_text_edit_text.setDisabled(True)
            self._spin_box_symbols_in_row.setDisabled(True)
            self._line_edit_image_path.setDisabled(False)
            self._button_load_image.setDisabled(False)

    def _load_image(self):
        ...

    def _load_key(self):
        _caption = 'Выбрать файл'
        _directory = ''
        _filter = 'Zip Archive (*.zip) ;; 7-Zip Archive (*.7z)'
        # Получаем путь к файлу ключа
        key_path = QFileDialog.getOpenFileName(parent=self,
                                               caption=_caption, 
                                               directory=_directory, 
                                               filter=_filter)[0]
        self._font_symbols, self._font_symbols_images = pentor.load_key(key_path)
        self._line_edit_key_path.setText(key_path)

    def _start(self):
        if self._radio_button_decrypt.isChecked():
            ...
        else:
            self._encrypt()

    def _encrypt(self):
        if self._font_symbols is None or self._font_symbols_images is None:
            raise Exception('Choose the key first!')
        text = str(self._plain_text_edit_text.toPlainText())
        symbols_in_row = int(self._spin_box_symbols_in_row.value())
        pentor.encrypt(text=text, 
                       font_symbols=self._font_symbols, 
                       font_symbols_images=self._font_symbols_images, 
                       symbols_in_row=symbols_in_row)
