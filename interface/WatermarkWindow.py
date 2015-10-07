from PyQt4.QtGui import *
from intel import Watermarker
from interface.ProgressWindow import ProgressWindow


class WatermarkWindow(QWidget):
    def __init__(self, main, title_font_size, button_size_w, button_size_h, button_font_size, subtitle_font_size):
        super().__init__()

        self.main = main
        self.batcher = Watermarker()
        self.progressWindow = ProgressWindow(self.main, 'Dodawanie znaku wodnego', self.batcher, 32, 0, 0, 12, 22)

        # deklaracja napisow

        title = QLabel('Znak wodny')

        label_font = title.font()
        label_font.setPointSize(title_font_size)
        label_font.setBold(True)
        title.setFont(label_font)

        source_folder_label = QLabel('Folder źródłowy: ')
        dest_folder_label = QLabel('Folder docelowy: ')
        watermark_label = QLabel('Znak wodny: ')
        position_label = QLabel('Położenie: ')
        quality_label = QLabel('Jakość: ')

        self.source_path_label = QLabel('')
        self.dest_path_label = QLabel('')
        self.watermark_path_label = QLabel('')

        # deklaracja przyciskow

        back_but = QPushButton('wstecz')
        choose_source_but = QPushButton('Wybierz folder...')
        choose_dest_but = QPushButton('Wybierz folder...')
        choose_watermark = QPushButton('Wybierz plik...')
        import_but = QPushButton('Import ustawień...')
        export_but = QPushButton('Eksport ustawień...')
        go_but = QPushButton('GO!')

        go_but.setFixedSize(button_size_w, button_size_h)
        but_font = go_but.font()
        but_font.setPointSize(button_font_size)
        go_but.setFont(but_font)

        #drop-down list

        self.position_list = QComboBox()
        self.position_list.addItem('--- Wybierz opcje ---', '')
        self.position_list.addItem('lewa góra', 'top-left')
        self.position_list.addItem('prawa góra', 'top-right')
        self.position_list.addItem('prawy dół', 'bottom-right')
        self.position_list.addItem('lewy dół', 'bottom-left')
        self.position_list.setFixedWidth(150)

        #edit-liny
        self.quality_line = QLineEdit()

        # layout

        quality_layout = QHBoxLayout()
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_line)
        quality_layout.addStretch()

        title_layout = QHBoxLayout()
        title_layout.addWidget(back_but)
        title_layout.addWidget(title)
        title_layout.addStretch()

        choose_source_folder_layout = QHBoxLayout()
        choose_source_folder_layout.addWidget(source_folder_label)
        choose_source_folder_layout.addWidget(choose_source_but)
        choose_source_folder_layout.addWidget(self.source_path_label)
        choose_source_folder_layout.addStretch()
        
        choose_dest_folder_layout = QHBoxLayout()
        choose_dest_folder_layout.addWidget(dest_folder_label)
        choose_dest_folder_layout.addWidget(choose_dest_but)
        choose_dest_folder_layout.addWidget(self.dest_path_label)
        choose_dest_folder_layout.addStretch()

        choose_layout = QVBoxLayout()
        choose_layout.addLayout(choose_source_folder_layout)
        choose_layout.addLayout(choose_dest_folder_layout)

        watermark_file_layout = QHBoxLayout()
        watermark_file_layout.addWidget(watermark_label)
        watermark_file_layout.addWidget(choose_watermark)
        watermark_file_layout.addWidget(self.watermark_path_label)
        watermark_file_layout.addStretch()

        position_layout = QHBoxLayout()
        position_layout.addWidget(position_label)
        position_layout.addWidget(self.position_list)
        position_layout.addStretch()

        watermark_layout = QVBoxLayout()
        watermark_layout.addLayout(watermark_file_layout)
        watermark_layout.addLayout(position_layout)
        watermark_layout.addLayout(quality_layout)

        choose_watermark_layout = QHBoxLayout()
        choose_watermark_layout.addLayout(watermark_layout)
        choose_watermark_layout.addLayout(choose_layout)

        exp_imp_but_layout = QHBoxLayout()
        exp_imp_but_layout.addStretch(2)
        exp_imp_but_layout.addWidget(import_but)
        exp_imp_but_layout.addWidget(export_but)
        exp_imp_but_layout.addStretch(2)

        go_but_layout = QHBoxLayout()
        go_but_layout.addStretch()
        go_but_layout.addWidget(go_but)
        go_but_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addWidget(self.main.h_line())
        main_layout.addStretch()
        main_layout.addLayout(choose_watermark_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.main.h_line())
        main_layout.addStretch()
        main_layout.addLayout(exp_imp_but_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.main.h_line())
        main_layout.addStretch()
        main_layout.addLayout(go_but_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

        # podpiecia przyciskow

        choose_watermark.clicked.connect(self.choose_watermark_but_fun)
        back_but.clicked.connect(self.back_but_fun)
        choose_source_but.clicked.connect(self.choose_but_fun)
        choose_dest_but.clicked.connect(self.choose_dest_but_fun)
        import_but.clicked.connect(self.import_settings)
        export_but.clicked.connect(self.export_settings)

        go_but.clicked.connect(self.go_but_fun)

    def back_but_fun(self):
        self.main.windows_c.removeWidget(self.main.windows_c.currentWidget())

    @staticmethod
    def set_combobox(combobox, user_data):
        for index in range(combobox.count()):
            if combobox.itemData(index) == user_data:
                combobox.setCurrentIndex(index)

    def import_settings(self):
        try:
            prop_path = QFileDialog.getOpenFileName(self, "Wczytaj ustawienia...", self.main.get_home_dir())
            self.batcher.load_prop(prop_path)
            self.watermark_path_label.setText(str(self.batcher.prop['watermark_source']))
            self.quality_line.setText(str(self.batcher.prop['quality']))
            self.dest_path_label.setText(str(self.batcher.prop['destination']))
            self.set_combobox(self.position_list, self.batcher.prop['pasting_corner'])
        except ValueError as err:
            self.main.statusBar().showMessage(str(err), 3000)
        except FileNotFoundError:
            self.main.statusBar().showMessage("Błędnie wybrany plik", 3000)
        except NameError:
            self.main.statusBar().showMessage("Wczytano nieodpowiedni plik", 3000)

    def export_settings(self):
        try:
            self.batcher.set_prop('watermark_source', self.watermark_path_label.text())
            self.batcher.set_prop('quality', self.quality_line.text())
            self.batcher.set_prop('destination', self.dest_path_label.text())
            self.batcher.set_prop('pasting_corner', str(self.position_list.itemData(self.position_list.currentIndex())))
            prop_path = QFileDialog.getSaveFileName(self, "Zapisz ustawienia...", self.main.get_home_dir())
            self.batcher.save_prop(prop_path)
        except ValueError as err:
            self.main.statusBar().showMessage(str(err), 3000)
        except FileNotFoundError:
            self.main.statusBar().showMessage("Błędnie wybrany plik", 3000)

    def choose_but_fun(self):
        try:
            self.batcher.select_dir(
                QFileDialog.getExistingDirectory(self, "Wybierz folder źródłowy...", self.main.get_home_dir()))
            self.source_path_label.setText(self.batcher.path)
        except ValueError as err:
            self.main.statusBar().showMessage(str(err), 3000)
        except FileNotFoundError:
            self.main.statusBar().showMessage("Błędnie wybrany katalog", 3000)

    def choose_dest_but_fun(self):
        try:
            self.dest_path_label.setText(
                QFileDialog.getExistingDirectory(self, "Wybierz folder docelowy...", self.main.get_home_dir()))
        except FileNotFoundError:
            self.main.statusBar().showMessage("Błędnie wybrany katalog", 3000)

    def choose_watermark_but_fun(self):
        try:
            self.watermark_path_label.setText(
                QFileDialog.getOpenFileName(self, "Wybierz znak wodny...", self.main.get_home_dir()))
        except FileNotFoundError:
            self.main.statusBar().showMessage("Błędnie wybrany katalog", 3000)

    def go_but_fun(self):
        try:
            self.batcher.check_dir(self.batcher.path)
            self.batcher.set_prop('watermark_source', self.watermark_path_label.text())
            self.batcher.set_prop('quality', self.quality_line.text())
            self.batcher.set_prop('destination', self.dest_path_label.text())
            self.batcher.set_prop('pasting_corner', str(self.position_list.itemData(self.position_list.currentIndex())))
            self.batcher.start()
            self.main.windows_c.addWidget(self.progressWindow)
            self.main.windows_c.setCurrentWidget(self.progressWindow)
            self.progressWindow.start()
        except ValueError as err:
            self.main.statusBar().showMessage(str(err), 3000)
