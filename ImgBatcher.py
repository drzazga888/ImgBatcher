import getpass
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from interface.HomeWindow import HomeWindow


class Main(QMainWindow):

    @staticmethod
    def get_home_dir():
        return os.path.expanduser("~" + getpass.getuser())

    @staticmethod
    def h_line():
        toto = QFrame()
        toto.setFrameShape(QFrame.HLine)
        toto.setFrameShadow(QFrame.Sunken)
        return toto

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        # stos okien
        self.windows_c = QStackedWidget()
        self.setCentralWidget(self.windows_c)

        # ustawienia okna
        self.setWindowIcon(QIcon('app_ico.png'))  # ustawienie ikonki programu
        self.setWindowTitle('ImgBatcher')  # ustawienie tytulu okna
        self.resize(800, 600)  # ustawienie domyslnego rozmiaru okna
        self.center()

    # wsparcie wysrodkowania okna
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication([])

    main = Main()
    main.windows_c.addWidget(HomeWindow(main, 300, 22, 32))  # ustawienia okna HomeWindow
    main.show()

    app.exec_()
