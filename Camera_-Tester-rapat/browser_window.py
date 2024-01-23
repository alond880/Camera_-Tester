from PyQt5.QtWidgets import *

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QLabel
from PyQt5.uic.properties import QtGui

from image_window import ImageWindow


class BrowserWindow(QFileDialog):

    def __init__(self, parent=None):
        super().__init__()

        # layout = QVBoxLayout()
        self.layout = QVBoxLayout()


        # image button
        self.image_btn = QPushButton("select image")
        self.layout.addWidget(self.image_btn)

        # pix button
        self.pix_btn = QPushButton("select pixel output file")
        self.layout.addWidget(self.pix_btn)

        # start button
        self.start_btn = QPushButton("START")
        self.layout.addWidget(self.start_btn)

        self.setGeometry(500, 500, 350, 300)
        self.setLayout(self.layout)
        self.setWindowTitle("welcome")

