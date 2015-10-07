from PyQt4.QtGui import *
from intel import Renamer
from interface.ProgressWindow import ProgressWindow


class NameChangeWindow(QWidget):
    def __init__(self, main, title_font_size, button_size_w, button_size_h, button_font_size, subtitle_font_size):
        super().__init__()

        self.main = main
        self.batcher = Renamer()
        self.progressWindow = ProgressWindow(self.main, 'Zmiana nazwy', self.batcher, 32, 0, 0, 12, 22)

        # deklaracja napisow

        title = QLabel('Zmiena nazwy')

        label_font = title.font()
        label_font.setPointSize(title_font_size)
        label_font.setBold(True)
        title.setFont(label_font)

        self.folder_name_label = QLabel('')
        self.folder_dest_name_label = QLabel('')

        text_before_label = QLabel('Tekst początkowy: ')
        digits_amount_label = QLabel('Ilość cyfr: ')

        label_font.setPointSize(subtitle_font_size)

        # deklaracja przyciskow

        back_but = QPushButton('wstecz')
        choose_but = QPushButton('Wybierz folder...')
        import_but = QPushButton('Import ustawień...')
        export_but = QPushButton('Export ustawień...')
        go_but = QPushButton('GO!')
        renaming_preview = QPushButton('Wygeneruj podgląd')

        go_but.setFixedSize(button_size_w, button_size_h)
        but_font = go_but.font()
        but_font.setPointSize(button_font_size)
        go_but.setFont(but_font)

        # deklaracja editline'ow

        self.text_before_line = QLineEdit()
        self.digits_amount_line = QLineEdit()

        # deklaracja listy mianiturek

        self.miniature_list = QListView()
        self.miniature_list_model = QStandardItemModel()
        self.miniature_list.setModel(self.miniature_list_model)
        self.miniature_list.setMinimumHeight(100)

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

        text_before_layout = QHBoxLayout()
        text_before_layout.addWidget(text_before_label)
        text_before_layout.addWidget(self.text_before_line)
        text_before_layout.addStretch()

        left_layout = QVBoxLayout()
        left_layout.addLayout(import_layout)
        left_layout.addLayout(text_before_layout)

        digits_amount_layout = QHBoxLayout()
        digits_amount_layout.addWidget(digits_amount_label)
        digits_amount_layout.addWidget(self.digits_amount_line)
        digits_amount_layout.addStretch()

        right_layout = QVBoxLayout()
        right_layout.addLayout(export_layout)
        right_layout.addLayout(digits_amount_layout)

        left_right_layout = QHBoxLayout()
        left_right_layout.addLayout(left_layout)
        left_right_layout.addLayout(right_layout)

        preview_layout = QHBoxLayout()
        preview_layout.addStretch()
        preview_layout.addWidget(renaming_preview)
        preview_layout.addStretch()

        go_but_layout = QHBoxLayout()
        go_but_layout.addStretch()
        go_but_layout.addWidget(go_but)
        go_but_layout.addStretch()

        miniature_list_layout = QHBoxLayout()
        miniature_list_layout.addWidget(self.miniature_list)

        main_layout = QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addWidget(self.main.h_line())
        main_layout.addLayout(choose_folder_layout)
        main_layout.addWidget(self.main.h_line())
        main_layout.addLayout(left_right_layout)
        main_layout.addLayout(preview_layout)
        main_layout.addLayout(miniature_list_layout)
        main_layout.addWidget(self.main.h_line())
        main_layout.addLayout(go_but_layout)

        self.setLayout(main_layout)

        # podpiecia przyciskow

        back_but.clicked.connect(self.back_but_fun)
        choose_but.clicked.connect(self.choose_but_fun)
        renaming_preview.clicked.connect(self.generate_preview)
        import_but.clicked.connect(self.import_settings)
        export_but.clicked.connect(self.export_settings)

        go_but.clicked.connect(self.go_but_fun)

    def import_settings(self):
        try:
            prop_path = QFileDialog.getOpenFileName(self, "Wczytaj ustawienia...", self.main.get_home_dir())
            self.batcher.load_prop(prop_path)
            self.text_before_line.setText(str(self.batcher.prop['text']))
            self.digits_amount_line.setText(str(self.batcher.prop['digits']))
        except ValueError as err:
            self.main.statusBar().showMessage(str(err), 3000)
        except FileNotFoundError:
            self.main.statusBar().showMessage("Błędnie wybrany plik", 3000)
        except NameError:
            self.main.statusBar().showMessage("Wczytano nieodpowiedni plik", 3000)

    def export_settings(self):
        try:
            self.batcher.set_prop('text', self.text_before_line.text())
            self.batcher.set_prop('digits', self.digits_amount_line.text())
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

    def generate_preview(self):
        self.miniature_list_model.clear()
        try:
            self.batcher.set_prop('text', self.text_before_line.text())
            self.batcher.set_prop('digits', self.digits_amount_line.text())
            self.batcher.create_transformation_schema()
            for entry in self.batcher.transformation_schema_str.split('\n'):
                item = QStandardItem(entry)
                self.miniature_list_model.appendRow(item)
        except ValueError as err:
            self.main.statusBar().showMessage(str(err), 3000)

    def go_but_fun(self):
        try:
            self.batcher.check_dir(self.batcher.path)
            self.batcher.set_prop('text', self.text_before_line.text())
            self.batcher.set_prop('digits', self.digits_amount_line.text())
            self.batcher.start()
            self.main.windows_c.addWidget(self.progressWindow)
            self.main.windows_c.setCurrentWidget(self.progressWindow)
            self.progressWindow.start()
        except ValueError as err:
            self.main.statusBar().showMessage(str(err), 3000)
