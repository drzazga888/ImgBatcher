from PyQt4.QtGui import *


class CompleteWindow(QWidget):
    def __init__(self, main, name, title_font_size, button_size_w, button_size_h, button_font_size, subtitle_font_size):
        super().__init__()

        self.main = main

        # deklaracja napisow

        title = QLabel(name)
        label_font = title.font()
        label_font.setPointSize(title_font_size)
        label_font.setBold(True)
        title.setFont(label_font)

        header = QLabel('Zrobione :)')
        header_font = header.font()
        header_font.setPointSize(title_font_size * 2)
        header.setFont(header_font)

        # deklaracja przyciskow

        back_but = QPushButton('wstecz')

        # layout

        title_layout = QHBoxLayout()
        title_layout.addWidget(title)
        title_layout.addStretch()

        header_layout = QHBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(header)
        header_layout.addStretch()

        back_layout = QHBoxLayout()
        back_layout.addStretch()
        back_layout.addWidget(back_but)
        back_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addLayout(header_layout)
        main_layout.addLayout(back_layout)

        self.setLayout(main_layout)

        # podpiecia przyciskow

        back_but.clicked.connect(self.back_but_fun)

    # info - nie będzie czyszczenia bo tworzony jest zawsze nowy batcher gdy wybierzemy coś z maina
    def back_but_fun(self):
        self.main.windows_c.removeWidget(self.main.windows_c.currentWidget())
        self.main.windows_c.removeWidget(self.main.windows_c.currentWidget())
