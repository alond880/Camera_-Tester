import sys
from PyQt5.QtWidgets import QApplication
from browser_window import BrowserWindow
from pyqt_connections import PyQtConnections

if __name__ == '__main__':
    app = QApplication(sys.argv)

    conn_obj = PyQtConnections()
    conn_obj.ui_obj.browser.show()

    app.exec_()