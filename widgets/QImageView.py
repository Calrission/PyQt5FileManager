from PyQt5.QtWidgets import QWidget, QLabel
from common.UtilsVisual import UtilsVisual


class QImageView(QWidget):
    def __init__(self, parent, path: str = None):
        super().__init__(parent=parent)

        self.click = None
        self.image = QLabel(self)
        self.image.resize(self.width(), self.height())
        self.path = path

    def resize(self, w: int, h: int):
        super().resize(w, h)
        self.image.resize(w, h)
        self._setImage(self.path)

    def _setImage(self, path: str):
        UtilsVisual.load_file_to_label_with_scaled(path, self.image, (self.width(), self.height()))
        self.image.show()

    def setImage(self, path: str):
        self.path = path
        self._setImage(path)

    def set_click(self, click):
        self.click = click