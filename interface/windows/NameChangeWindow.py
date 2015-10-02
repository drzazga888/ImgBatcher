from PyQt4.QtGui import *
from PyQt4 import QtCore


class NameChangeWindow(QWidget):

    def __init__(self, main, title_font_size, button_size_w, button_size_h, button_font_size, subtitle_font_size):
        super().__init__()

        self.main = main
        self.folder_name = None
        self.miniature_name_list = []

        # deklaracja napisow

        title = QLabel('Zmiena nazwy')

        label_font = title.font()
        label_font.setPointSize(title_font_size)
        label_font.setBold(True)
        title.setFont(label_font)

        paragraph1 = QLabel('1. Wskaż folder z obrazkami')
        self.folder_name_label = QLabel('')
        self.folder_dest_name_label = QLabel('')

        paragraph2 = QLabel('2. Ustaw właściwości')
        sort_label = QLabel('Sortuj wg... ')
        text_before_label = QLabel('Tekst początkowy: ')
        digits_amount_label = QLabel('Ilość cyfr: ')
        preview_label = QLabel('podgląd')

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

        label_font = preview_label.font()
        label_font.setPointSize(subtitle_font_size)
        preview_label.setFont(label_font)

        # deklaracja przyciskow

        back_but = QPushButton('wstecz')
        choose_but = QPushButton('Wybierz folder...')
        import_but = QPushButton('Import ustawień...')
        go_but = QPushButton('GO!')

        go_but.setFixedSize(button_size_w, button_size_h)
        but_font = go_but.font()
        but_font.setPointSize(button_font_size)
        go_but.setFont(but_font)

        # deklaracja editline'ow

        self.text_before_line = QLineEdit()
        self.digits_amount_line = QLineEdit()

        # deklaracja listy rozwijanej

        self.sort_type_list = QComboBox()
        self.sort_type_list.setEditable(True)
        self.sort_type_list.addItems(['--- Wybierz opcje ---', 'Nazwa'])
        self.sort_type_list.setFixedWidth(150)
        self.sort_type_list.lineEdit().setAlignment(QtCore.Qt.AlignCenter)

        # deklaracja listy mianiturek

        self.miniature_list = QListView()
        self.miniature_list_model = QStandardItemModel(self.miniature_list)
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
        
        sort_layout = QHBoxLayout()
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_type_list)
        sort_layout.addStretch()

        left_layout = QVBoxLayout()
        left_layout.addLayout(import_layout)
        left_layout.addLayout(sort_layout)

        text_before_layout = QHBoxLayout()
        text_before_layout.addWidget(text_before_label)
        text_before_layout.addWidget(self.text_before_line)
        text_before_layout.addStretch()

        digits_amount_layout = QHBoxLayout()
        digits_amount_layout.addWidget(digits_amount_label)
        digits_amount_layout.addWidget(self.digits_amount_line)
        digits_amount_layout.addStretch()

        right_layout = QVBoxLayout()
        right_layout.addLayout(text_before_layout)
        right_layout.addLayout(digits_amount_layout)

        left_right_layout = QHBoxLayout()
        left_right_layout.addLayout(left_layout)
        left_right_layout.addLayout(right_layout)

        preview_layout = QHBoxLayout()
        preview_layout.addStretch()
        preview_layout.addWidget(preview_label)
        preview_layout.addStretch()

        go_but_layout = QHBoxLayout()
        go_but_layout.addStretch()
        go_but_layout.addWidget(go_but)
        go_but_layout.addStretch()

        miniature_list_layout = QHBoxLayout()
        miniature_list_layout.addWidget(self.miniature_list)

        main_layout = QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addWidget(paragraph1)
        main_layout.addLayout(choose_folder_layout)
        main_layout.addWidget(paragraph2)
        main_layout.addLayout(left_right_layout)
        main_layout.addLayout(preview_layout)
        main_layout.addLayout(miniature_list_layout)
        main_layout.addWidget(paragraph3)
        main_layout.addLayout(go_but_layout)

        self.setLayout(main_layout)

        # podpiecia przyciskow

        back_but.clicked.connect(self.back_but_fun)
        choose_but.clicked.connect(self.choose_but_fun)

        go_but.clicked.connect(self.go_but_fun)

    def back_but_fun(self):
        # TODO wyczyscic dane przed wykonaniem wstecz
        self.main.windows_c.removeWidget(self.main.windows_c.currentWidget())

    def choose_but_fun(self):
        try:
            new_file_name = self.text_before_line.text()
            for val in {
                new_file_name.find('/'),
                new_file_name.find('\\'),
                new_file_name.find('?'),
                new_file_name.find(':'),
                new_file_name.find('*'),
                new_file_name.find('"'),
                new_file_name.find('>'),
                new_file_name.find('<'),
                new_file_name.find('|')
                # \ / ? : * " > < |
            }:
                if val != -1:
                    raise ValueError('Illegal sign in filename!')

            digits_amount = int(self.digits_amount_line.text())

        except ValueError as valErr:
            self.main.statusBar().showMessage('Uzupełnij (poprawnie) formularze. ' +
                                              (str(valErr) if str(valErr) == 'Illegal sign in filename!' else '')
                                              , 3000)
            return

        self.miniature_list_model.clear()
        self.folder_name = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.folder_name_label.setText(self.folder_name)

        import os
        i = 0
        for path, subdirs, files in os.walk(self.folder_name):
            for filename in files:
                extension = os.path.splitext(filename)[1].lower()
                if extension in {'.jpg', '.tiff', '.png', '.bmp'}:
                    new_file_basename = os.path.basename(new_file_name)
                    self.miniature_name_list.append((filename, new_file_basename+str(i).zfill(digits_amount)+extension))

                    item = QStandardItem(self.miniature_name_list[-1][0]+" ---> "+self.miniature_name_list[-1][1])
                    self.miniature_list_model.appendRow(item)
                    i += 1

    def go_but_fun(self):
        try:
            if not self.folder_name:
                raise ValueError()
        except ValueError:
            self.main.statusBar().showMessage('Uzupełnij (poprawnie) formularze', 3000)
            return

        from interface.go_exec_fun import change_names
        if change_names(self.folder_name, self.miniature_name_list):
            QMessageBox.information(self, 'Done', 'Zrobione :-)')
            self.main.windows_c.removeWidget(self.main.windows_c.currentWidget())
        else:
            QMessageBox.information(self, 'Error', 'Błąd :-(\n\njakiś głupi opis błędu makaarena makaarena\n'
                                                      'makaarena makaarena makaarena \n'
                                                      'makaarena makaarena makaarena ')