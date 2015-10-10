from PyQt5.QtWidgets import *

from interface.NameChangeWindow import NameChangeWindow
from interface.CreateMiniatureWindow import CreateMiniatureWindow
from interface.WatermarkWindow import WatermarkWindow


class HomeWindow(QWidget):

    def __init__(self, main, button_size, button_font_size, title_font_size):
        super().__init__()

        self.main = main

        # deklaracja tytulu

        title = QLabel('ImgBatcher')

        font_title = title.font()
        font_title.setPointSize(title_font_size)
        font_title.setBold(True)
        title.setFont(font_title)

        # deklaracje przyciskow

        create_but = QPushButton('Miniatury')
        change_name_but = QPushButton('Zmiana nazw')
        watermark_but = QPushButton('Znak wodny')

        create_but.setFixedSize(button_size, button_size)
        change_name_but.setFixedSize(button_size, button_size)
        watermark_but.setFixedSize(button_size, button_size)

        but_font = create_but.font()
        but_font.setPointSize(button_font_size)
        create_but.setFont(but_font)

        but_font = change_name_but.font()
        but_font.setPointSize(button_font_size)
        change_name_but.setFont(but_font)

        but_font = watermark_but.font()
        but_font.setPointSize(button_font_size)
        watermark_but.setFont(but_font)

        # layout

        but_box_layout = QHBoxLayout()
        but_box_layout.addStretch()
        but_box_layout.addWidget(create_but)
        but_box_layout.addWidget(change_name_but)
        but_box_layout.addWidget(watermark_but)
        but_box_layout.addStretch()

        title_box_layout = QHBoxLayout()
        title_box_layout.addStretch()
        title_box_layout.addWidget(title)
        title_box_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addLayout(title_box_layout)
        main_layout.addStretch()
        main_layout.addLayout(but_box_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

        # podpiecia przyciskow

        create_but.clicked.connect(self.create_but_fun)
        change_name_but.clicked.connect(self.change_name_but_fun)
        watermark_but.clicked.connect(self.watermark_but_fun)

    def create_but_fun(self):
        createMiniatureWindow = CreateMiniatureWindow(self.main, 32, 200, 100, 18, 18)  # ustawienia okna CreateMiniatureWindow
        self.main.windows_c.addWidget(createMiniatureWindow)
        self.main.windows_c.setCurrentWidget(createMiniatureWindow)

    def change_name_but_fun(self):
        nameChangeWindow = NameChangeWindow(self.main, 32, 200, 100, 18, 18)  # ustawienia okna NameChangeWindow
        self.main.windows_c.addWidget(nameChangeWindow)
        self.main.windows_c.setCurrentWidget(nameChangeWindow)

    def watermark_but_fun(self):
        watermarkWindow = WatermarkWindow(self.main, 32, 200, 100, 18, 18)  # ustawienia okna NameChangeWindow
        self.main.windows_c.addWidget(watermarkWindow)
        self.main.windows_c.setCurrentWidget(watermarkWindow)