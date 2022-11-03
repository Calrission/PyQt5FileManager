from PyQt5.QtWidgets import QWidget
from widgets.QImageView import QImageView
from widgets.QSmartWidget import QSmartWidget


class QOverlay(QSmartWidget):
    def __init__(self, x: int, y: int, parent: QWidget):
        self.image_background = None
        super().__init__(x, y, parent)

    def initUI(self):
        self._init_background(self.width(), self.height())

    def _init_background(self, w: int, h: int):
        self.image_background = QImageView(self, path="files/back_tag_select.png")
        self.image_background.mousePressEvent = lambda x: None
        self.image_background.resize(w, h)
        self.image_background.lower()
