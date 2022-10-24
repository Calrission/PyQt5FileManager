from PyQt5.QtWidgets import *
from PathObjects import PathObject
from UtilsVisual import UtilsVisual


class QOverlay(QWidget):
    def __init__(self, x: int, y: int, parent: QWidget):
        self.x = x
        self.y = y
        self.background = None
        super().__init__(parent)

    def _calc_x_y(self, x, y):
        new_x = x if x + self.width() <= self.parent().width() else x - self.width()
        new_y = y if y + self.height() <= self.parent().height() else y - self.height()
        self.x, self.y = new_x, new_y

    def show(self) -> None:
        self.initUI()
        self.move(self.x, self.y)
        self.raise_()
        super().show()

    def initUI(self):
        pass

    def _init_background(self, w: int, h: int):
        self.background = QLabel(self)
        UtilsVisual.load_file_to_label_with_scaled("files/back_tag_select.png", self.background,
                                                   (w, h))
        self.background.resize(w, h)
        self.background.lower()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x=}, {self.y=})"


class QActionPathObject(QOverlay):
    def __init__(self, path_object: PathObject, x: int, y: int, parent: QWidget):
        super().__init__(x, y, parent)
        self.path_object = path_object

    def initUI(self):
        open_label = QLabel(self)
        open_label.setText("Открыть")

        pre_open_label = QLabel(self)
        pre_open_label.setText("Предпросмотр")

        rename_label = QLabel(self)
        rename_label.setText("Переименовать")

        delete_label = QLabel(self)
        delete_label.setText("Удалить")

        info_label = QLabel(self)
        info_label.setText("Свойства")

        open_label.setStyleSheet("QLabel { color: rgb(255, 255, 255); }")
        pre_open_label.setStyleSheet("QLabel { color: rgb(255, 255, 255); }")
        rename_label.setStyleSheet("QLabel { color: rgb(255, 255, 255); }")
        delete_label.setStyleSheet("QLabel { color: rgb(255, 255, 255); }")
        info_label.setStyleSheet("QLabel { color: rgb(255, 255, 255); }")

        open_label.move(5, 0)
        pre_open_label.move(5, 20)
        rename_label.move(5, 40)
        delete_label.move(5, 60)
        info_label.move(5, 80)

        super().initUI()
        self._init_background(80, 100)

