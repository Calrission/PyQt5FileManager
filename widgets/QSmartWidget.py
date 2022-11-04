from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui


class QSmartWidget(QWidget):
    def __init__(self, x: int, y: int, parent: QWidget):
        self.x = x
        self.y = y
        super().__init__(parent)

    def _calc_x_y(self, x, y, w, h):
        new_x = x if x + w <= self.parent().width() else abs(x - w)
        new_y = y if y + h <= self.parent().height() else abs(y - h)
        if new_y >= 0 and new_x >= 0:
            self.x, self.y = new_x, new_y
        else:
            self.x, self.y = x, y

    def show(self) -> None:
        self.initUI()
        self.move(self.x, self.y)
        self.raise_()
        super().show()

    def initUI(self):
        pass

    def move_calc_x_y(self, w, h):
        self._calc_x_y(self.x, self.y, w, h)
        self.move(self.x, self.y)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        a0.size()
        self.move_calc_x_y(a0.size().width(), a0.size().height())

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x=}, {self.y=})"