from PyQt5.QtWidgets import *
from interface.ProgressWindow import ProgressWindow
from intel import *


class CreateMiniatureWindow(QWidget):
    def __init__(self, main, title_font_size, button_size_w, button_size_h, button_font_size, subtitle_font_size):
        super().__init__()

        self.batcher = Resizer()
        self.main = main
        self.progressWindow = ProgressWindow(self.main, 'Stwórz miniatury', self.batcher, 32, 0, 0, 12, 22)

        # deklaracja napisow

        title = QLabel('Stwórz miniatury')

        label_font = title.font()
        label_font.setPointSize(title_font_size)
        label_font.setBold(True)
        title.setFont(label_font)

        self.folder_name_label = QLabel('')
        self.folder_dest_name_label = QLabel('')

        width_label = QLabel('Szerokość: ')
        height_label = QLabel('Wysokość: ')
        folder_dest_label = QLabel('Folder docelowy: ')
        quality_label = QLabel('Jakość: ')


        # deklaracja przyciskow

        back_but = QPushButton('wstecz')
        choose_but = QPushButton('Wybierz folder...')
        import_but = QPushButton('Import ustawień...')
        export_but = QPushButton('Eksport ustawień...')
        choose_dest_but = QPushButton('Wybierz...')
        go_but = QPushButton('GO!')

        go_but.setFixedSize(button_size_w, button_size_h)
        but_font = go_but.font()
        but_font.setPointSize(button_font_size)
        go_but.setFont(but_font)

        # deklaracja editline'ow

        self.width_line = QLineEdit()
        self.height_line = QLineEdit()
        self.quality_line = QLineEdit()

        self.width_line.setFixedWidth(50)
        self.height_line.setFixedWidth(50)
        self.quality_line.setFixedWidth(50)

        # layout

        title_layout = QHBoxLayout()
        title_layout.addWidget(back_but)
        title_layout.addWidget(title)
        title_layout.addStretch()

        choose_folder_layout = QHBoxLayout()
        choose_folder_layout.addWidget(choose_but)
        choose_folder_layout.addWidget(self.folder_name_label)
        choose_folder_layout.addStretch()

        import_layout = QHBoxLayout()
        import_layout.addWidget(import_but)
        import_layout.addStretch()

        export_layout = QHBoxLayout()
        export_layout.addWidget(export_but)
        export_layout.addStretch()

        width_layout = QHBoxLayout()
        width_layout.addWidget(width_label)
        width_layout.addWidget(self.width_line)
        width_layout.addWidget(QLabel('px'))
        width_layout.addStretch()

        height_layout = QHBoxLayout()
        height_layout.addWidget(height_label)
        height_layout.addWidget(self.height_line)
        height_layout.addWidget(QLabel('px'))
        height_layout.addStretch()

        left_layout = QVBoxLayout()
        left_layout.addLayout(import_layout)
        left_layout.addLayout(width_layout)
        left_layout.addLayout(height_layout)

        folder_dest_layout = QHBoxLayout()
        folder_dest_layout.addWidget(folder_dest_label)
        folder_dest_layout.addWidget(choose_dest_but)
        folder_dest_layout.addWidget(self.folder_dest_name_label)
        folder_dest_layout.addStretch()

        quality_layout = QHBoxLayout()
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_line)
        quality_layout.addStretch()

        right_layout = QVBoxLayout()
        right_layout.addLayout(export_layout)
        right_layout.addLayout(folder_dest_layout)
        right_layout.addLayout(quality_layout)

        left_right_layout = QHBoxLayout()
        left_right_layout.addLayout(left_layout)
        left_right_layout.addLayout(right_layout)

        go_but_layout = QHBoxLayout()
        go_but_layout.addStretch()
        go_but_layout.addWidget(go_but)
        go_but_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addWidget(self.main.h_line())
        main_layout.addLayout(choose_folder_layout)
        main_layout.addWidget(self.main.h_line())
        main_layout.addLayout(left_right_layout)
        main_layout.addWidget(self.main.h_line())
        main_layout.addLayout(go_but_layout)

        self.setLayout(main_layout)

        # podpiecia przyciskow

        back_but.clicked.connect(self.back_but_fun)
        choose_but.clicked.connect(self.choose_but_fun)
        choose_dest_but.clicked.connect(self.choose_dest_but_fun)
        import_but.clicked.connect(self.import_settings)
        export_but.clicked.connect(self.export_settings)

        go_but.clicked.connect(self.go_but_fun)

    def import_settings(self):
        try:
            prop_path = QFileDialog.getOpenFileName(self, "Wczytaj ustawienia...", self.main.get_home_dir())
            self.batcher.load_prop(prop_path)
            self.width_line.setText(str(self.batcher.prop['size'][0]))
            self.height_line.setText(str(self.batcher.prop['size'][1]))
            self.quality_line.setText(str(self.batcher.prop['quality']))
            self.folder_dest_name_label.setText(str(self.batcher.prop['destination']))
        except ValueError as err:
            self.main.statusBar().showMessage(str(err), 3000)
        except FileNotFoundError:
            self.main.statusBar().showMessage("Błędnie wybrany plik", 3000)
        except NameError:
            self.main.statusBar().showMessage("Wczytano nieodpowiedni plik", 3000)

    def export_settings(self):
        try:
            self.batcher.set_prop('size', (self.width_line.text(), self.height_line.text()))
            self.batcher.set_prop('quality', self.quality_line.text())
            self.batcher.set_prop('destination', self.folder_dest_name_label.text())
            prop_path = QFileDialog.getSaveFileName(self, "Zapisz ustawienia...", self.main.get_home_dir())
            self.batcher.save_prop(prop_path)
        except ValueError as err:
            self.main.statusBar().showMessage(str(err), 3000)
        except FileNotFoundError:
            self.main.statusBar().showMessage("Błędnie wybrany plik", 3000)

    def back_but_fun(self):
        self.main.windows_c.removeWidget(self.main.windows_c.currentWidget())

    def choose_but_fun(self):
        try:
            self.batcher.select_dir(
                QFileDialog.getExistingDirectory(self, "Wybierz folder źródłowy...", self.main.get_home_dir()))
            self.folder_name_label.setText(self.batcher.path)
        except ValueError as err:
            self.main.statusBar().showMessage(str(err), 3000)
        except FileNotFoundError:
            self.main.statusBar().showMessage("Błędnie wybrany katalog", 3000)

    def choose_dest_but_fun(self):
        try:
            self.folder_dest_name_label.setText(
                QFileDialog.getExistingDirectory(self, "Wybierz folder docelowy...", self.main.get_home_dir()))
        except FileNotFoundError:
            self.main.statusBar().showMessage("Błędnie wybrany katalog", 3000)

    def go_but_fun(self):
        try:
            self.batcher.check_dir(self.batcher.path)
            self.batcher.set_prop('size', (self.width_line.text(), self.height_line.text()))
            self.batcher.set_prop('quality', self.quality_line.text())
            self.batcher.set_prop('destination', self.folder_dest_name_label.text())
            self.batcher.start()
            self.main.windows_c.addWidget(self.progressWindow)
            self.main.windows_c.setCurrentWidget(self.progressWindow)
            self.progressWindow.start()
        except ValueError as err:
            self.main.statusBar().showMessage(str(err), 3000)
