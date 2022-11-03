from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui


class QSmartWidget(QWidget):
    def __init__(self, x: int, y: int, parent: QWidget):
        self.x = x
        self.y = y
        super().__init__(parent)

    def _calc_x_y(self, x, y):
        new_x = x if x + self.width() <= self.parent().width() else x - self.width()
        new_y = y if y + self.height() <= self.parent().height() else y - self.height()
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

    def move_calc_x_y(self):
        self._calc_x_y(self.x, self.y)
        self.move(self.x, self.y)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.move_calc_x_y()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x=}, {self.y=})"