from PyQt5.QtWidgets import QWidget

from .form import Ui_PentorForm


class PentorGUI(QWidget, Ui_PentorForm):
    """Графический пользовательский интерфейс для Pentor, созданный
    ради удобства пользования утилитой."""

    def __init__(self):
        """Инициализация графического пользовательского интерфейса"""
