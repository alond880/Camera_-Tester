import sys
import os
from math import sqrt
from PIL import Image
import cv2
from datetime import datetime
from datetime import date

import pyscreenshot
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PySide2 import QtCore, QtGui, QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel


class BrowserWindow(QFileDialog):

    def __init__(self, parent=None):
        super().__init__()

        self.layout = QVBoxLayout()

        self.image_fname = "default_image.png"
        self.pix_fname = ""

        # image button
        self.image_btn = QPushButton("select image")
        self.image_btn.clicked.connect(self.get_image_file)
        self.layout.addWidget(self.image_btn)
        self.image_button_le = QLabel("Hello")

        # pix button
        self.pix_btn = QPushButton("select pixel output file")
        self.pix_btn.clicked.connect(self.get_pix_file)
        self.layout.addWidget(self.pix_btn)
        self.pix_button_le = QLabel("Hello")

        # start button
        self.image_btn = QPushButton("START")
        self.image_btn.clicked.connect(self.start_app)
        self.layout.addWidget(self.image_btn)
        self.image_button_le = QLabel("Hello")

        self.setWindowIcon(QtGui.QIcon('MantakLogo.png'))
        self.setGeometry(500, 500, 350, 300)
        self.setLayout(self.layout)
        self.setWindowTitle("welcome")

    def get_image_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpg *.gif)")
        self.image_fname = fname[0]

    def get_pix_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Text files (*.txt)")
        self.pix_fname = fname[0]

    def start_app(self):
        self.image_window = ImageWindow(self.image_fname, self.pix_fname)
        self.image_window.show()


class ImageWindow(QMainWindow):

    def __init__(self, image_path, pix_path):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setWindowIcon(QtGui.QIcon('MantakLogo.png'))
        self.pix_file_name = self.get_file_name(pix_path)
        self.setWindowTitle(self.pix_file_name)

        # save button
        self.save_button = QPushButton('save', self)
        self.save_button.setToolTip('This is an example button')
        self.save_button.setGeometry(0, 455, 80, 20)
        self.save_button.clicked.connect(self.save_results)

        # This is the ugliest piece of shit I have ever written.
        # But... bossman wants this ready by tomorrow.
        self.area1_l0 = QLabel("", self)
        self.area1_l1 = QLabel("", self)
        self.area1_l2 = QLabel("", self)
        self.area1_l3 = QLabel("", self)

        self.area1_r0 = QtGui.QRegion(160, 120, 80, 240)
        self.area1_r1 = QtGui.QRegion(400, 120, 80, 240)
        self.area1_r2 = QtGui.QRegion(240, 120, 160, 40)
        self.area1_r3 = QtGui.QRegion(240, 280, 160, 80)

        self.area2_l0 = QLabel("", self)
        self.area2_l1 = QLabel("", self)
        self.area2_l2 = QLabel("", self)
        self.area2_l3 = QLabel("", self)

        self.area2_r0 = QtGui.QRegion(0, 0, 160, 480)
        self.area2_r1 = QtGui.QRegion(480, 0, 160, 480)
        self.area2_r2 = QtGui.QRegion(160, 0, 320, 120)
        self.area2_r3 = QtGui.QRegion(160, 360, 320, 120)

        # area = [xPos, yPos, width, length]
        self.area0 = [240, 160, 160, 120]  # center
        self.area1 = [160, 120, 320, 240]  # middle
        self.area2 = [0, 0, 640, 480]  # large

        self.r0 = QtGui.QRegion(self.area0[0], self.area0[1], self.area0[2], self.area0[3])
        self.r1 = QtGui.QRegion(self.area1[0], self.area1[1], self.area1[2], self.area1[3])
        self.r2 = QtGui.QRegion(self.area2[0], self.area2[1], self.area2[2], self.area2[3])

        self.area0_count = 0
        self.area1_count = 0
        self.area2_count = 0

        self.area0_result = "passed"  # failed/ passed
        self.area1_result = "passed"  # failed/ passed
        self.area2_result = "passed"  # failed/ passed

        self.max_pixels0 = 5  # 5
        self.max_pixels1 = 40  # 40
        self.max_pixels2 = 150  # 150

        self.area0_fill_label = QLabel("", self)
        self.area1_fill_label = QLabel("", self)
        self.area2_fill_label = QLabel("", self)

        # area0 count label
        self.count_label0 = QLabel("0", self)
        self.count_label0.setGeometry(self.area0[0], self.area0[1], 35, 15)
        self.count_label0.setStyleSheet("background-color: red")
        self.count_label0.setFont(QFont('Arial', 14))

        # area1 count label
        self.count_label1 = QLabel("0", self)
        self.count_label1.setGeometry(self.area1[0], self.area1[1], 35, 15)
        self.count_label1.setStyleSheet("background-color: yellow")
        self.count_label1.setFont(QFont('Arial', 14))

        # area2 count label
        self.count_label2 = QLabel("0", self)
        self.count_label2.setGeometry(self.area2[0], self.area2[1], 35, 15)
        self.count_label2.setStyleSheet("background-color: lightblue")
        self.count_label2.setFont(QFont('Arial', 14))

        self.image_fname = image_path
        self.pix_fname = pix_path
        self.setGeometry(30, 30, 640, 480)  # (30, 30, 640, 480)

        self.textbox = QLineEdit(self)
        self.textbox.move(0, 0)
        self.textbox.resize(1, 1)

        self.pix_splited = []
        self.pixels_splitted = []
        self.failed_pixels = []
        self.lumps = []

        self.read_pix_file()
        self.dead_pixels_check()
        self.failed_pixels_runthrough()

    def get_file_name(self, string):
        newstring = ""
        length = len(string)

        for i in range(length - 1, 0, -1):
            if (string[i] == "/"):
                return newstring[::-1]
            else:
                newstring = newstring + string[i]

    @staticmethod
    def remove_empty(val):
        if not val:
            return False
        else:
            return True

    def check_failed_check(self):
        if self.area0_count > self.max_pixels0:
            # self.failed_test("איזור פנימי")
            self.area0_fill_label.setGeometry(self.r0.boundingRect())
            self.area0_fill_label.setText("")
            self.area0_fill_label.setStyleSheet("background-color: rgba(255, 0, 0, 40);")
            self.area0_fill_label.update()
            self.area0_result = "failed"

        if self.area1_count > self.max_pixels1:
            # self.failed_test("איזור אמצעי")

            self.area1_l0.setGeometry(self.area1_r0.boundingRect())
            self.area1_l0.setStyleSheet("background-color: rgba(255,255,0, 40);")
            self.area1_l0.update()

            self.area1_l1.setGeometry(self.area1_r1.boundingRect())
            self.area1_l1.setStyleSheet("background-color: rgba(255, 255, 0, 40);")
            self.area1_l1.update()

            self.area1_l2.setGeometry(self.area1_r2.boundingRect())
            self.area1_l2.setStyleSheet("background-color: rgba(255, 255, 0, 40);")
            self.area1_l2.update()

            self.area1_l3.setGeometry(self.area1_r3.boundingRect())
            self.area1_l3.setStyleSheet("background-color: rgba(255, 255, 0, 40);")
            self.area1_l3.update()

            self.area1_result = "failed"

        if self.area2_count > self.max_pixels2:

            self.area2_l0.setGeometry(self.area2_r0.boundingRect())
            self.area2_l0.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
            self.area2_l0.update()

            self.area2_l1.setGeometry(self.area2_r1.boundingRect())
            self.area2_l1.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
            self.area2_l1.update()

            self.area2_l2.setGeometry(self.area2_r2.boundingRect())
            self.area2_l2.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
            self.area2_l2.update()

            self.area2_l3.setGeometry(self.area2_r3.boundingRect())
            self.area2_l3.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
            self.area2_l3.update()

            self.area2_result = "failed"

    def cut_image(self, image_path):
        img = Image.open(image_path)

        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        x = self.pos().x()
        y = self.pos().y()

        x1 = x
        y1 = y + height

        x2 = x + width
        y2 = y

        #print(x1, y1, x2, y2)
        # box = (x1, y1, x2, y2)
        box = (x, y, x + width, y + height)
        img2 = img.crop(box)
        img2.save('screenshot_finale.jpg')
        os.remove("screenshot.jpg")

    def save_results(self):
        f = open("results.txt", "w+")
        f.truncate(0)

        screen = QtWidgets.QApplication.primaryScreen()
        #p = screen.grabWindow(self.pos().x(), self.pos().y(), 640, 480)
        p = screen.grabWindow(0, 0, -1, -1) # screenshot entire screen
        p.save("Screenshot.jpg", 'jpg')
        self.cut_image("Screenshot.jpg")

        now = datetime.now() # current date and time
        time = now.strftime("%H:%M")
        date = str(datetime.today().day) + ':' + str(datetime.today().month) + ':' + str(datetime.today().year)

        if self.pix_file_name is None:
            self.pix_file_name = "No file chosen"

        f.write(self.pix_file_name + "  " + str(time) + ' ' + date + ' :' + '\n')
        f.write("area0: " + str(self.area0_count) + " pixels - " + self.area0_result + '\n')
        f.write("area1: " + str(self.area1_count) + " pixels - " + self.area1_result + '\n')
        f.write("area2: " + str(self.area2_count) + " pixels - " + self.area2_result + '\n')

        print("saved result to: results.txt")

    # returns TRUE if linear distance between pixels is larger then 1
    def calc_linear_distance(self, x0, x1, y0, y1):
        if sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2) <= sqrt(2):
            return True
        else:
            return False

    # finds lumps of dead pixels on image
    def failed_pixels_runthrough(self):
        count = 0
        self.pixels_splitted = list(filter(self.remove_empty, self.pixels_splitted))

        for i, (y, x) in enumerate(self.pixels_splitted):
            prev_pix = self.calc_linear_distance(x, self.pixels_splitted[i - 1][1], y, self.pixels_splitted[i - 1][0])
            if i == len(self.pixels_splitted) - 1:
                next_pix = False
            else:
                next_pix = self.calc_linear_distance(x, self.pixels_splitted[i + 1][1], y,
                                                     self.pixels_splitted[i + 1][0])


            if prev_pix is False and next_pix is True:
                self.lumps.append((x, y))

            elif prev_pix is True and next_pix is False:
                self.lumps.append((x, y))
                self.lumps.append(('E', 'E'))

            elif prev_pix is True and next_pix is True:
                self.lumps.append((x, y))

        for i, (x, y) in enumerate(self.lumps):
            if (x, y) == ('E', 'E'):
                p = QPoint(self.lumps[i - 1][0], self.lumps[i - 1][1])

                if self.r0.contains(p):
                    self.area0_count += 1
                elif self.r1.contains(p):
                    self.area1_count += 1
                elif self.r2.contains(p):
                    self.area2_count += 1

            self.count_label0.setText(str(self.area0_count))
            self.count_label1.setText(str(self.area1_count))
            self.count_label2.setText(str(self.area2_count))

        # for i, (x, y) in enumerate(self.lumps):
        #     if (x, y) == ('E', 'E'):
        #         print(".")
        #     else:
        #         p = QPoint(x, y)
        #         if self.r1.contains(p):
        #             print((x, y))

        ######################
        for i, (x, y) in enumerate(self.lumps):
            if (x, y) != ('E', 'E'):
                p = QPoint(int(x), int(y))
                if self.r0.contains(p):
                    print(p)
        ######################


        self.check_failed_check()

    # finds individual dead pixels on image
    def dead_pixels_check(self):
        if not self.pixels_splitted:
            print('EMPTY')
            return
        self.pixels_splitted = list(filter(self.remove_empty, self.pixels_splitted))

        # linear distance calculation
        # y is first because of the input file ([y, x] instead of [x, y])
        for i, (y, x) in enumerate(self.pixels_splitted):
            for j, (y2, x2) in enumerate(self.pixels_splitted[:i]):
                if sqrt((x - x2) ** 2 + (y - y2) ** 2) <= sqrt(2):
                    self.failed_pixels.append((x, y))

    def read_pix_file(self):
        try:
            f = open(self.pix_fname, "r")
            self.pix = f.readlines()
            for line in self.pix:
                self.pix_splited = [int(s) for s in str.split(line) if s.isdigit()]
                self.pixels_splitted.append(self.pix_splited)
        except:
            print("no file chosen")
            self.pix = ""

    def paint_dot(self, x, y, color, thick):
        # print(x, y)
        pen = QPen(color, thick)
        self.painter.setPen(pen)
        self.painter.drawPoint(x, y)

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.begin(self)
        self.pixmap = QPixmap(self.image_fname)
        self.painter.drawPixmap(self.rect(), self.pixmap)

        # area0
        pen = QPen(Qt.red, 2)
        self.painter.setPen(pen)
        self.painter.drawRect(self.r0.boundingRect())
        # self.area0_fill_label.setStyleSheet("background-color: rgba(255, 0, 0, 40);")

        # area1
        pen = QPen(Qt.yellow, 2)
        self.painter.setPen(pen)
        self.painter.drawRect(self.r1.boundingRect())

        # area2
        pen = QPen(Qt.blue, 2)
        self.painter.setPen(pen)
        self.painter.drawRect(self.r2.boundingRect())

        # pixels (blue dots)
        for line in self.pix:
            self.pix_splited = [int(s) for s in str.split(line) if s.isdigit()]
            try:  # x                    y
                self.paint_dot(self.pix_splited[1], self.pix_splited[0], Qt.blue, 3)
            except:
                continue
        #
        # # red dots
        # for (x, y) in self.failed_pixels:
        #     self.paint_dot(x, y, Qt.red, 3)
        # # print('done painting')

        # lumps (red dots)
        for (x, y) in self.lumps:
            if (x, y) != ('E', 'E'):
                self.paint_dot(x, y, Qt.red, 3)
        # print('done painting')

        self.painter.end()

    # check if pixel is in which area
    def check_area0(self, x, y):
        p = QPoint(x, y)
        return self.r0.contains(p)

    def check_area1(self, x, y):
        p = QPoint(x, y)
        return self.r1.contains(p)

    def check_area2(self, x, y):
        p = QPoint(x, y)
        return self.r2.contains(p)

    def failed_test(self, failed_area):
        self.textbox.text()
        QMessageBox.question(self, 'נכשל', "חרג מכמות הפיקסלים המתים המקסימלית: " + failed_area, QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")

    def mouseDoubleClickEvent(self, event):
        print(event.x(), event.y())

        p = QPoint(event.x(), event.y())

        if self.r0.contains(p):
            self.area0_count += 1
            self.count_label0.setText(str(self.area0_count))

        elif self.r1.contains(p):
            self.area1_count += 1
            self.count_label1.setText(str(self.area1_count))

        elif self.r2.contains(p):
            self.area2_count += 1
            self.count_label2.setText(str(self.area2_count))

        self.check_failed_check()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    browser = BrowserWindow()
    browser.show()

    app.exec_()
