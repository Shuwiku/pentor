import os
import webbrowser

from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget

import config
import pentor
from .form import Ui_PentorForm


def _message_box_confirm(text, title):
    message_box = QMessageBox()
    message_box.addButton('Да', QMessageBox.YesRole)
    message_box.addButton('Нет', QMessageBox.NoRole)
    message_box.setIcon(QMessageBox.Question)
    message_box.setText(text)
    message_box.setWindowIcon(QtGui.QIcon(config.ICON_FILE))
    message_box.setWindowTitle(title)
    return message_box.exec_()


def _message_box_critical(text, title):
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Critical)
    message_box.setText(text)
    message_box.setWindowIcon(QtGui.QIcon(config.ICON_FILE))
    message_box.setWindowTitle(title)
    return message_box.exec_()


class PentorGUI(QWidget, Ui_PentorForm):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon(config.ICON_FILE))
        self._setup_buttons()
        self._setup_radio_buttons()

    def _setup_buttons(self):
        self._button_about.clicked.connect(self._about)
        self._button_load_image.clicked.connect(self._load_image)
        self._button_load_key.clicked.connect(self._load_key)
        self._button_start.clicked.connect(self._start)

    def _setup_radio_buttons(self):
        self._radio_button_decrypt.toggled.connect(self._change_mode)
        self._radio_button_encrypt.setChecked(True)
        self._change_mode()

    def _about(self):
        is_open = _message_box_confirm('Открыть страницу проекта на GitHub?', 'О проекте')
        if is_open == 0:
            webbrowser.open(config.GITHUB_PAGE)

    def _change_mode(self):
        self._set_decrypt_mode() if self._radio_button_decrypt.isChecked() \
            else self._set_encrypt_mode()

    def _load_image(self):
        _filter = 'PNG Image (*.png)'
        path = QFileDialog.getOpenFileName(parent=self,
                                           caption='Выбрать изображение с зашифрованным текстом',
                                           directory='',
                                           filter=_filter)[0]
        self._line_edit_image_path.setText(path)

    def _load_key(self):
        _filter = 'Zip Archive (*.zip) ;; 7-Zip Archive (*.7z)'
        path = QFileDialog.getOpenFileName(parent=self,
                                           caption='Выбрать файл ключа',
                                           directory='',
                                           filter=_filter)[0]
        self._line_edit_key_path.setText(path)

    def _pentor_decrypt(self):
        image_path = self._line_edit_image_path.text()
        key_path = self._line_edit_key_path.text()
        pentor.decrypt(image_path=image_path,
                       key_path=key_path)
        os.system('pentor.txt')

    def _pentor_encrypt(self):
        key_path = self._line_edit_key_path.text()
        text = self._plain_text_edit_text.toPlainText()
        copy_image_scale = None
        if self._check_box_add_image_copy.isChecked():
            buttons = [(self._radio_button_x2, 2), (self._radio_button_x4, 4),
                       (self._radio_button_x8, 8), (self._radio_button_x16, 16)]
            for button, scale in buttons:
                if button.isChecked():
                    copy_image_scale = scale
                    break
        delete_bad_symbols = self._check_box_delete_bad_symbols.isChecked()
        symbols_in_row = self._spin_box_symbols_in_row.value()
        text_case = None
        if self._check_box_text_to_single_case.isChecked():
            if self._radio_button_lower.isChecked():
                text_case = 'lower'
            else:
                text_case = 'upper'
        pentor.encrypt(copy_image_scale=copy_image_scale,
                       delete_bad_symbols=delete_bad_symbols,
                       key_path=key_path,
                       symbols_in_row=symbols_in_row,
                       text=text,
                       text_case=text_case)
        os.system('pentor.png')

    def _set_decrypt_mode(self):
        self._plain_text_edit_text.setDisabled(True)
        self._spin_box_symbols_in_row.setDisabled(True)
        self._line_edit_image_path.setDisabled(False)
        self._button_load_image.setDisabled(False)

    def _set_encrypt_mode(self):
        self._line_edit_image_path.setDisabled(True)
        self._button_load_image.setDisabled(True)
        self._plain_text_edit_text.setDisabled(False)
        self._spin_box_symbols_in_row.setDisabled(False)

    def _start(self):
        if self._radio_button_decrypt.isChecked():
            try:
                self._pentor_decrypt()
            except Exception as e:
                _message_box_critical(str(e), 'Ошибка')
        else:
            try:
                self._pentor_encrypt()
            except Exception as e:
                _message_box_critical(str(e), 'Ошибка')
