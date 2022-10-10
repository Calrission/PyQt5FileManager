from PyQt5.QtWidgets import *
from UtilsVisual import UtilsVisual
from ConstValues import *
from enum import Enum


class TypeHistoryButton(Enum):
    LEFT = ["files/left_d.png", "files/left_e.png"]
    RIGHT = ["files/right_d.png", "files/right_e.png"]


class QHistoryButton(QWidget):
    def __init__(self, parent, type_: TypeHistoryButton):
        super().__init__(parent=parent)

        self.resize(WIDTH_HISTORY_BUTTON, HEIGHT_HISTORY_BUTTON)

        self.states = type_.value
        self.click = None
        self.image = QLabel(self)
        self.image.resize(self.width(), self.height())
        self.mousePressEvent = lambda x: (self.click() if self.click is not None else None)
        self.setEnabled(False)

    def setEnabled(self, bool_: bool):
        super().setEnabled(bool_)
        self._setImage(self.states[int(bool_)])

    def _setImage(self, path: str):
        UtilsVisual.load_file_to_label_with_scaled(path, self.image, (self.width(), self.height()))
        self.image.show()

    def set_click(self, click):
        self.click = click
