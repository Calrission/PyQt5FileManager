from PyQt5.QtWidgets import QWidget
from PathObjects import PathObject


class QOverlay(QWidget):
    def __init__(self, x, y, parent):
        super().__init__(parent)
        self.move(*self._calc_x_y(x, y))

    def _calc_x_y(self, x, y):
        new_x = x if x + self.width() <= self.parent().width() else x - self.width()
        new_y = y if y + self.height() <= self.parent().height() else y - self.height()
        return new_x, new_y

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x()=}, {self.y()=})"


class QActionPathObject(QOverlay):
    def __init__(self, path_object: PathObject, x: int, y: int, parent: QWidget):
        self.x = x
        self.y = y
        self.path_object = path_object
        self.initUI()
        super().__init__(x, y, parent)

    def initUI(self):
        pass
