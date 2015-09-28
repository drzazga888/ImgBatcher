from PyQt4.QtGui import *


class CreateMiniatureWindow(QWidget):

    def __init__(self, main, title_font_size, button_size_w, button_size_h, button_font_size, subtitle_font_size):
        super().__init__()

        self.main = main
        self.folder_name = None
        self.folder_dest_name = None

        # deklaracja napisow

        title = QLabel('Stwórz miniatury')

        label_font = title.font()
        label_font.setPointSize(title_font_size)
        label_font.setBold(True)
        title.setFont(label_font)

        paragraph1 = QLabel('1. Wskaż folder z obrazkami')
        self.folder_name_label = QLabel('')
        self.folder_dest_name_label = QLabel('')

        paragraph2 = QLabel('2. Ustaw właściwości')
        width_label = QLabel('Szerokość: ')
        heigh_label = QLabel('Wysokość: ')
        folder_dest_label = QLabel('Folder docelowy: ')
        sharpen_label = QLabel('Wyostrzenie: ')
        quality_label = QLabel('Jakość: ')

        paragraph3 = QLabel('3. Wykonaj')

        label_font = paragraph1.font()
        label_font.setPointSize(subtitle_font_size)
        paragraph1.setFont(label_font)

        label_font = paragraph2.font()
        label_font.setPointSize(subtitle_font_size)
        paragraph2.setFont(label_font)

        label_font = paragraph3.font()
        label_font.setPointSize(subtitle_font_size)
        paragraph3.setFont(label_font)

        # deklaracja przyciskow

        back_but = QPushButton('wstecz')
        choose_but = QPushButton('Wybierz folder...')
        import_but = QPushButton('Import ustawień...')
        choose_dest_but = QPushButton('Wybierz...')
        go_but = QPushButton('GO!')

        go_but.setFixedSize(button_size_w, button_size_h)
        but_font = go_but.font()
        but_font.setPointSize(button_font_size)
        go_but.setFont(but_font)

        # deklaracja radiobutton'ow

        self.sharpen_rbut = QRadioButton()

        #deklaracja editline'ow

        self.width_line = QLineEdit()
        self.heigh_line = QLineEdit()
        self.quality_line = QLineEdit()

        self.width_line.setFixedWidth(50)
        self.heigh_line.setFixedWidth(50)
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

        width_layout = QHBoxLayout()
        width_layout.addWidget(width_label)
        width_layout.addWidget(self.width_line)
        width_layout.addWidget(QLabel('px'))
        width_layout.addStretch()

        heigh_layout = QHBoxLayout()
        heigh_layout.addWidget(heigh_label)
        heigh_layout.addWidget(self.heigh_line)
        heigh_layout.addWidget(QLabel('px'))
        heigh_layout.addStretch()

        left_layout = QVBoxLayout()
        left_layout.addLayout(import_layout)
        left_layout.addLayout(width_layout)
        left_layout.addLayout(heigh_layout)

        folder_dest_layout = QHBoxLayout()
        folder_dest_layout.addWidget(folder_dest_label)
        folder_dest_layout.addWidget(choose_dest_but)
        folder_dest_layout.addWidget(self.folder_dest_name_label)
        folder_dest_layout.addStretch()

        sharpen_layout = QHBoxLayout()
        sharpen_layout.addWidget(sharpen_label)
        sharpen_layout.addWidget(self.sharpen_rbut)
        sharpen_layout.addStretch()

        quality_layout = QHBoxLayout()
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_line)
        quality_layout.addStretch()

        right_layout = QVBoxLayout()
        right_layout.addLayout(folder_dest_layout)
        right_layout.addLayout(sharpen_layout)
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
        main_layout.addWidget(paragraph1)
        main_layout.addLayout(choose_folder_layout)
        main_layout.addWidget(paragraph2)
        main_layout.addLayout(left_right_layout)
        main_layout.addWidget(paragraph3)
        main_layout.addLayout(go_but_layout)

        self.setLayout(main_layout)
        
        # podpiecia przyciskow

        back_but.clicked.connect(self.back_but_fun)
        choose_but.clicked.connect(self.choose_but_fun)
        choose_dest_but.clicked.connect(self.choose_dest_but_fun)

        go_but.clicked.connect(self.go_but_fun)

    def back_but_fun(self):
        # TODO wyczyscic dane przed wykonaniem wstecz
        self.main.windows_c.removeWidget(self.main.windows_c.currentWidget())

    def choose_but_fun(self):
        self.folder_name = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.folder_name_label.setText(self.folder_name)

    def choose_dest_but_fun(self):
        self.folder_dest_name = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.folder_dest_name_label.setText(self.folder_dest_name)

    def go_but_fun(self):
        # TODO zabezpieczenie na ujemne wartosci
        try:
            width = int(self.width_line.text())
            heigh = int(self.heigh_line.text())
            quality = int(self.quality_line.text())
            if not self.folder_name or not self.folder_dest_name:
                raise ValueError()
        except ValueError:
            self.main.statusBar().showMessage('Uzupełnij (poprawnie) formularze', 3000)
            return

        is_sharpen = self.sharpen_rbut.isChecked()

        from interface.go_exec_fun import change_miniature_size
        if change_miniature_size(width, heigh, quality, self.folder_name, self.folder_dest_name, is_sharpen):
            QMessageBox.information(self, 'Done', 'Zrobione :-)')
            self.main.windows_c.removeWidget(self.main.windows_c.currentWidget())
        else:
            QMessageBox.information(self, 'Error', 'Błąd :-(\n\njakiś głupi opis błędu makaarena makaarena\n'
                                                      'makaarena makaarena makaarena \n'
                                                      'makaarena makaarena makaarena ')