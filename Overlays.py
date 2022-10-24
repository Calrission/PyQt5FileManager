from PyQt5.QtWidgets import *
from PathObjects import PathObject
from UtilsVisual import UtilsVisual


class QOverlay(QWidget):
    def __init__(self, x: int, y: int, parent: QWidget):
        self.x = x
        self.y = y
        super().__init__(parent)

    def _calc_x_y(self, x, y):
        new_x = x if x + self.width() <= self.parent().width() else x - self.width()
        new_y = y if y + self.height() <= self.parent().height() else y - self.height()
        self.x, self.y = new_x, new_y

    def show(self) -> None:
        self.move(self.x, self.y)
        self.raise_()
        super().show()

    def initUI(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x=}, {self.y=})"


class QActionPathObject(QOverlay):
    def __init__(self, path_object: PathObject, x: int, y: int, parent: QWidget):
        super().__init__(x, y, parent)
        self.icon = None
        self.path_object = path_object

    def initUI(self):
        self.resize(100, 100)
        self.icon = QLabel(self)
        UtilsVisual.load_file_to_label_with_scaled("files/icon", self.icon, (self.width(), self.height()))

    def show(self):
        self.initUI()
        super().show()

