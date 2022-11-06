from PyQt5.QtWidgets import QWidget

from widgets.QImageBackground import QImageBackground
from widgets.QImageView import QImageView
from widgets.QSmartWidget import QSmartWidget


class QOverlay(QSmartWidget):
    def __init__(self, x: int, y: int, parent: QWidget):
        self._background = None
        super().__init__(x, y, parent)

    def initUI(self):
        self._background = QImageBackground(self, "files/back_tag_select.png")
        self._init_background(self.width(), self.height())

    def _init_background(self, w, h):
        self._background.init_background(w, h)
        self._background.lower()
