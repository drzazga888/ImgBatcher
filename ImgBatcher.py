from interface.windows.HomeWindow import HomeWindow

from PyQt4.QtGui import *


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        # stos okien
        self.windows_c = QStackedWidget()
        self.setCentralWidget(self.windows_c)

        # ustawienia okna
        # self.setWindowIcon(QIcon('app_ico.png'))  # ustawienie ikonki programu
        self.setWindowTitle('Window title <Kamil will change this>')  # ustawienie tytulu okna
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
