from PyQt5.QtWidgets import *
from UtilsVisual import UtilsVisual
from ConstValues import *
from enum import Enum


class TypeImageButton(Enum):
    LEFT = ["files/left_d.png", "files/left_e.png"]
    RIGHT = ["files/right_d.png", "files/right_e.png"]
    SETTINGS = ["files/setting_d.png", "files/setting.png"]


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


class QSwitchImageButton(QImageView):
    def __init__(self, parent, type_: TypeImageButton):
        super().__init__(parent=parent)

        self.resize(WIDTH_BUTTON, HEIGHT_BUTTON)

        self.states = type_.value
        self.mousePressEvent = lambda x: (self.click() if self.click is not None else None)
        self.setEnabled(False)

    def setEnabled(self, bool_: bool):
        super().setEnabled(bool_)
        self._setImage(self.states[int(bool_)])

    def setImage(self, path: str):
        try:
            index = self.states.index(path)
        except IndexError:
            index = 0
        self.setEnabled(bool(index))


