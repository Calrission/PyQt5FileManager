from PyQt5.QtWidgets import QWidget


class QOverlay(QWidget):
    def __init__(self, x, y, parent):
        super().__init__(parent)
        self.move(*self._calc_x_y(x, y))

    def _calc_x_y(self, x, y):
        new_x = x if x + self.width() <= self.parent().width() else x - self.width()
        new_y = y if y + self.height() <= self.parent().height() else y - self.height()
        return new_x, new_y
