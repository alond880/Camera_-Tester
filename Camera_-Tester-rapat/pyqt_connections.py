from browser_window import BrowserWindow
from image_window import ImageWindow
from backend import BackEnd
from ui import UI

class PyQtConnections:
    def __init__(self):

        # create UI and Backend objects, as well as window objects
        self.browser = BrowserWindow()
        self.image_window = ImageWindow()
        self.backend = BackEnd(self.browser, self.image_window)
        self.ui_obj = UI(self.browser, self.image_window)


        self.init_conn()

    def browser_conn(self):
        self.ui_obj.browser.image_btn.clicked.connect(self.backend.get_image_file)
        self.ui_obj.browser.pix_btn.clicked.connect(self.backend.get_pix_file)
        self.ui_obj.browser.start_btn.clicked.connect(self.backend.start_app)

    def image_conn(self):
        pass

    def init_conn(self):
        self.browser_conn()
