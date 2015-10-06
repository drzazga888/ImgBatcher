from PyQt4 import QtCore
from PyQt4.QtGui import *
from intel import Batcher
from interface.CompleteWindow import CompleteWindow


class ProgressWindow(QWidget):

    out_of_delimiter = "/"
    init_processed_label = '?/?'

    def __init__(self, main, name, batcher, title_font_size, bar_size_w, bar_size_h, button_font_size, subtitle_font_size):
        super().__init__()

        self.main = main
        self.batcher = batcher
        self.timer = QtCore.QBasicTimer()
        self.completeWindow = CompleteWindow(self.main, name, 32, 200, 100, 18, 18)

        # deklaracja napisow

        title = QLabel('Zmiena nazwy')
        label_font = title.font()
        label_font.setPointSize(title_font_size)
        label_font.setBold(True)
        title.setFont(label_font)

        bar_title = QLabel('Wykonywanie...')
        label_font = bar_title.font()
        label_font.setPointSize(subtitle_font_size)
        bar_title.setFont(label_font)

        self.proc_img_label = QLabel(self.init_processed_label)
        self.delimiter = '/'

        self.proc_img_label.setFixedWidth(40)

        # deklaracja przyciskow

        cancel_but = QPushButton('anuluj')

        but_font = cancel_but.font()
        but_font.setPointSize(button_font_size)
        cancel_but.setFont(but_font)

        #deklaracja

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(25)

        # layout

        title_layout = QHBoxLayout()
        title_layout.addWidget(title)
        title_layout.addStretch()

        subtitle_layout = QHBoxLayout()
        subtitle_layout.addStretch()
        subtitle_layout.addWidget(bar_title)
        subtitle_layout.addStretch()

        progress_bar_layout = QHBoxLayout()
        progress_bar_layout.addStretch()
        progress_bar_layout.addWidget(self.progress_bar)
        progress_bar_layout.addStretch()

        proc_layout = QHBoxLayout()
        proc_layout.addStretch()
        proc_layout.addWidget(self.proc_img_label)
        proc_layout.addStretch()

        cancel_but_layout = QVBoxLayout()
        cancel_but_layout.addStretch()
        cancel_but_layout.addWidget(cancel_but)
        cancel_but_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addStretch()
        main_layout.addLayout(subtitle_layout)
        main_layout.addLayout(progress_bar_layout)
        main_layout.addLayout(proc_layout)
        main_layout.addStretch()
        main_layout.addLayout(cancel_but_layout)

        self.setLayout(main_layout)

        # podpiecia przyciskow

        cancel_but.clicked.connect(self.cancel_but_fun)

    def cancel_but_fun(self):
        self.timer.stop()
        self.batcher.stop()
        self.main.windows_c.removeWidget(self.main.windows_c.currentWidget())
        self.main.windows_c.removeWidget(self.main.windows_c.currentWidget())

    def set_progress(self, processed, total):
        self.progress_bar.setValue(processed * 100 / total)
        self.proc_img_label.setText(str(processed) + self.out_of_delimiter + str(total))

    def timerEvent(self, e):
        if not self.batcher.isRunning():
            self.timer.stop()
            self.main.windows_c.addWidget(self.completeWindow)
            self.main.windows_c.setCurrentWidget(self.completeWindow)
            return
        self.set_progress(self.batcher.processed, self.batcher.total)

    def start(self):
        self.timer.start(Batcher.wait_time_ms, self)
