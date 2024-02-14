from PyQt5.QtGui import QColor

default_img = r"white.jpg"
# default_pix = r"adjacent.txt"
# default_pix = r"aaaa.txt"
default_pix = r"empty.txt"

# max groups for each adjacent type for al areas
max_pixels0 = [1, 0, 0, 0, 0]
max_pixelsA = [5, 4, 0, 0, 0]
max_pixelsB = [50, 40, 0, 0, 0]
max_pixelsC = [150, 50, 5, 1, 1]

TYPE1_COLOR = QColor('orange')
TYPE2_COLOR = QColor('green')
TYPE3_COLOR = QColor('yellow')
TYPE4_COLOR = QColor('gray')
TYPE5_COLOR = QColor('purple')

CIRCLE_RAD_ENHANCE = 2

ROW_LENGTH = 480
COLUMN_LENGTH = 640