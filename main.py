import sys
from PyQt5.QtWidgets import QApplication
from form import MainForm


def main():
    app = QApplication(sys.argv)
    win = MainForm()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
