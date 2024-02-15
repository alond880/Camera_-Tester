from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow

import params


class ImageWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('MantakLogo.png'))
        self.setWindowTitle("Topaz Testing GUI")

        # This is the ugliest piece of shit I have ever written.
        # But... boris wants this ready by tomorrow.
        self.areaA_l0 = QLabel("", self)
        self.areaA_l1 = QLabel("", self)
        self.areaA_l2 = QLabel("", self)
        self.areaA_l3 = QLabel("", self)

        # self.areaA = [240, 180, 160, 120]  # center
        self.areaA_r0 = QtGui.QRegion(240, 180, 160, 50)
        self.areaA_r1 = QtGui.QRegion(240, 250, 160, 50)
        self.areaA_r2 = QtGui.QRegion(240, 230, 70, 20)
        self.areaA_r3 = QtGui.QRegion(330, 230, 70, 20)

        self.areaB_l0 = QLabel("", self)
        self.areaB_l1 = QLabel("", self)
        self.areaB_l2 = QLabel("", self)
        self.areaB_l3 = QLabel("", self)

        # self.areaB = [160, 120, 320, 240]  # middle
        self.areaB_r0 = QtGui.QRegion(160, 120, 80, 240)
        self.areaB_r1 = QtGui.QRegion(400, 120, 80, 240)
        self.areaB_r2 = QtGui.QRegion(240, 120, 160, 60)
        self.areaB_r3 = QtGui.QRegion(240, 300, 160, 60)

        self.areaC_l0 = QLabel("", self)
        self.areaC_l1 = QLabel("", self)
        self.areaC_l2 = QLabel("", self)
        self.areaC_l3 = QLabel("", self)

        self.areaC_r0 = QtGui.QRegion(0, 0, 160, 480)
        self.areaC_r1 = QtGui.QRegion(480, 0, 160, 480)
        self.areaC_r2 = QtGui.QRegion(160, 0, 320, 120)
        self.areaC_r3 = QtGui.QRegion(160, 360, 320, 120)

        # area = [xPos, yPos, width, length]
        self.area0 = [310, 230, 20, 20]  # small center
        self.areaA = [240, 180, 160, 120]  # center
        self.areaB = [160, 120, 320, 240]  # middle
        self.areaC = [0, 0, 640, 480]  # large

        self.r0 = QtGui.QRegion(self.area0[0], self.area0[1], self.area0[2], self.area0[3])
        self.rA = QtGui.QRegion(self.areaA[0], self.areaA[1], self.areaA[2], self.areaA[3])
        self.rB = QtGui.QRegion(self.areaB[0], self.areaB[1], self.areaB[2], self.areaB[3])
        self.rC = QtGui.QRegion(self.areaC[0], self.areaC[1], self.areaC[2], self.areaC[3])

        # 6 elements: 5 for each adjacent type +1 for mouseclick user addups
        self.area0_count = [0] * 6
        self.areaA_count = [0] * 6
        self.areaB_count = [0] * 6
        self.areaC_count = [0] * 6

        self.area0_fill_label = QLabel("", self)

        # area0 count label
        # self.count_label0 = QLabel("0", self)
        # self.count_label0.setGeometry(self.area0[0] - 15, self.area0[1] - 15, 15, 15)
        # self.count_label0.setStyleSheet("background-color: red")
        # self.count_label0.setFont(QFont('Arial', 14))
        #
        # # areaA count label
        # self.count_labelA = QLabel("0", self)
        # self.count_labelA.setGeometry(self.areaA[0], self.areaA[1], 35, 15)
        # self.count_labelA.setStyleSheet("background-color: red")
        # self.count_labelA.setFont(QFont('Arial', 14))
        #
        # # areaB count label
        # self.count_labelB = QLabel("0", self)
        # self.count_labelB.setGeometry(self.areaB[0], self.areaB[1], 35, 15)
        # self.count_labelB.setStyleSheet("background-color: yellow")
        # self.count_labelB.setFont(QFont('Arial', 14))
        #
        # # areaB count label
        # self.count_labelC = QLabel("0", self)
        # self.count_labelC.setGeometry(self.areaC[0], self.areaC[1], 35, 15)
        # self.count_labelC.setStyleSheet("background-color: lightblue")
        # self.count_labelC.setFont(QFont('Arial', 14))

        # pass/fail label
        self.pass_fail_label = QLabel(self)
        self.pass_fail_label.setText("Pass")
        self.pass_fail_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.pass_fail_label.setStyleSheet("color: red;")
        self.pass_fail_label.setGeometry(10, 10, 300, 40)  # Adjust the size and position as needed
        self.pass_fail_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.pass_fail_label.setHidden(True)  # Set the label as hidden initially

        self.image_fname = params.default_img
        self.pix_fname = params.default_pix
        self.setGeometry(30, 30, 640, 480)

        self.textbox = QLineEdit(self)
        self.textbox.move(0, 0)
        self.textbox.resize(1, 1)

        # self.clicked_pix_arr = [[0, 0]]
        self.pix_splited = []
        self.pixels_splitted = []
        self.failed_pixels = []
        self.red_dots = []
        self.circles = []  # containes all circles dictionarys, not in any order, made only for drawing purposes

        self.painter = QPainter()
        self.pixmap = QPixmap(self.image_fname)
        self.pen = None
        self.pix = ""

    @staticmethod
    def remove_empty(val):
        if not val:
            return False
        else:
            return True

    def paint_dot(self, x, y, color, thick):
        pen = QPen(color, thick)
        self.painter.setPen(pen)
        self.painter.drawPoint(x, y)

    def paint_circle(self, x, y, rad, color, thick=1):
        pen = QPen(color, thick)
        self.painter.setPen(pen)
        self.painter.drawEllipse(x, y, rad, rad)

    def paint_red_dots(self):
        # self.red_dots is constructed from arrays each containing (x, y) coordinates of different types (meaning costumer requirements types)
        # for arr in self.red_dots:S
        for (x, y) in self.red_dots:
            # self.paint_circle(x, y, 20, QColor("red"))
            self.paint_dot(x, y, Qt.red, 3)

    def paint_circles(self):
        for circle in self.circles:
            self.paint_circle(int(circle["center"][0]), int(circle["center"][1]), circle["rad"], circle["color"])


    def paintEvent(self, event):
        self.pixmap.load(self.image_fname)

        self.painter = QPainter(self)
        self.painter.begin(self)
        self.pixmap = QPixmap(self.image_fname)
        self.painter.drawPixmap(self.rect(), self.pixmap)

        # area0
        pen = QPen(Qt.green, 2)
        self.painter.setPen(pen)
        self.painter.drawRect(self.r0.boundingRect())

        # areaA
        pen = QPen(Qt.red, 2)
        self.painter.setPen(pen)
        self.painter.drawRect(self.rA.boundingRect())

        # areaB
        pen = QPen(Qt.yellow, 2)
        self.painter.setPen(pen)
        self.painter.drawRect(self.rB.boundingRect())

        # areaC
        pen = QPen(Qt.blue, 2)
        self.painter.setPen(pen)
        self.painter.drawRect(self.rC.boundingRect())

        # blue dots
        for line in self.pix:
            self.pix_splited = [int(s) for s in str.split(line) if s.isdigit()]
            if len(self.pix_splited) > 0:
                try:  # self.pix_splited[1]: x, self.pix_splited[0]: y
                    self.paint_dot(self.pix_splited[1], self.pix_splited[0], Qt.blue, 3)
                except Exception as e:
                    print(self.pix_splited[1], self.pix_splited[0], e)


        self.paint_red_dots()
        self.paint_circles()
        self.painter.end()

    """
    mouseDoubleClickEvent handles double cliking on image.
    meaning it used to handle user addin-ins to the pixel count.
    disabled in new version.
    """
    # def mouseDoubleClickEvent(self, event):
    #     print('  %d  %d' % (event.y(), event.x()))
    #
    #     p = QPoint(event.x(), event.y())
    #
    #     if self.r0.contains(p):
    #         self.area0_count[5] += 1
    #         self.count_label0.setText(str(sum(self.area0_count)))
    #
    #     elif self.rA.contains(p):
    #         self.areaA_count[5] += 1
    #         self.count_labelA.setText(str(sum(self.areaA_count)))
    #
    #     elif self.rB.contains(p):
    #         self.areaB_count[5] += 1
    #         self.count_labelB.setText(str(sum(self.areaB_count)))
    #
    #     elif self.rC.contains(p):
    #         self.areaC_count[5] += 1
    #         self.count_labelC.setText(str(sum(self.areaC_count)))
    #
    #     if self.area0_count > params.max_pixels0:
    #         self.area0_fill_label.setGeometry(self.r0.boundingRect())
    #         self.area0_fill_label.setText("")
    #         self.area0_fill_label.setStyleSheet("background-color: rgba(0, 255, 0, 40);")
    #         self.area0_fill_label.update()
    #
    #     if self.areaA_count > params.max_pixelsA:
    #         self.areaA_l0.setGeometry(self.areaA_r0.boundingRect())
    #         self.areaA_l0.setStyleSheet("background-color: rgba(255,0,0, 40);")
    #         self.areaA_l0.update()
    #
    #         self.areaA_l1.setGeometry(self.areaA_r1.boundingRect())
    #         self.areaA_l1.setStyleSheet("background-color: rgba(255, 0, 0, 40);")
    #         self.areaA_l1.update()
    #
    #         self.areaA_l2.setGeometry(self.areaA_r2.boundingRect())
    #         self.areaA_l2.setStyleSheet("background-color: rgba(255, 0, 0, 40);")
    #         self.areaA_l2.update()
    #
    #         self.areaA_l3.setGeometry(self.areaA_r3.boundingRect())
    #         self.areaA_l3.setStyleSheet("background-color: rgba(255, 0, 0, 40);")
    #         self.areaA_l3.update()
    #
    #     if self.areaB_count > params.max_pixelsB:
    #         self.areaB_l0.setGeometry(self.areaB_r0.boundingRect())
    #         self.areaB_l0.setStyleSheet("background-color: rgba(255,255,0, 40);")
    #         self.areaB_l0.update()
    #
    #         self.areaB_l1.setGeometry(self.areaB_r1.boundingRect())
    #         self.areaB_l1.setStyleSheet("background-color: rgba(255, 255, 0, 40);")
    #         self.areaB_l1.update()
    #
    #         self.areaB_l2.setGeometry(self.areaB_r2.boundingRect())
    #         self.areaB_l2.setStyleSheet("background-color: rgba(255, 255, 0, 40);")
    #         self.areaB_l2.update()
    #
    #         self.areaB_l3.setGeometry(self.areaB_r3.boundingRect())
    #         self.areaB_l3.setStyleSheet("background-color: rgba(255, 255, 0, 40);")
    #         self.areaB_l3.update()
    #
    #     if self.areaC_count > params.max_pixelsC:
    #         # self.failed_test("איזור חיצוני")
    #
    #         self.areaC_l0.setGeometry(self.areaC_r0.boundingRect())
    #         self.areaC_l0.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
    #         self.areaC_l0.update()
    #
    #         self.areaC_l1.setGeometry(self.areaC_r1.boundingRect())
    #         self.areaC_l1.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
    #         self.areaC_l1.update()
    #
    #         self.areaC_l2.setGeometry(self.areaC_r2.boundingRect())
    #         self.areaC_l2.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
    #         self.areaC_l2.update()
    #
    #         self.areaC_l3.setGeometry(self.areaC_r3.boundingRect())
    #         self.areaC_l3.setStyleSheet("background-color: rgba(0, 0, 255, 40);")
    #         self.areaC_l3.update()

    # check if pixel is in which area
    # def check_areaA(self, x, y):
    #     p = QPoint(x, y)
    #
    #     self.areaA_fill_label.setText(self.rA.contains(p))
    #     return self.rA.contains(p)
    #
    # def check_areaB(self, x, y):
    #     p = QPoint(x, y)
    #     return self.rB.contains(p)
    #
    # def check_areaC(self, x, y):
    #     p = QPoint(x, y)
    #     return self.rC.contains(p)
    #
    # def failed_test(self, failed_area):
    #     self.textbox.text()
    #     QMessageBox.question(self, 'נכשל', "חרג מכמות הפיקסלים המתים המקסימלית: " + failed_area, QMessageBox.Ok,
    #                          QMessageBox.Ok)
    #     self.textbox.setText("")
