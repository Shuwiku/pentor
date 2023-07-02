import sys

from PyQt5.QtWidgets import QApplication

from gui import PentorGUI


def main():
    app = QApplication(sys.argv)
    window = PentorGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
