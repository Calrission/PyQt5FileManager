from PyQt5 import Qt
from PyQt5.QtWidgets import QLabel

from common.UtilsVisual import UtilsVisual
from values.ConstValues import COLOR_TEXT, MARGIN_ITEM
from widgets.QImageBackground import QImageBackground


class QImageButton(QImageBackground):
    def __init__(self, parent, text: str):
        super().__init__(parent, "files/back_tag_select")
        self.text = text
        self.label_text = QLabel(self.text)
        self.label_text.setParent(self)
        UtilsVisual.set_color_text(self.label_text, COLOR_TEXT)
        self.label_text.setAlignment(Qt.Qt.AlignCenter)
        self.label_text.show()
        self.resize(self.width(), self.height())

    def _resize_label(self, w: int, h: int):
        self.label_text.resize(w, h)
        self.label_text.move(self.width() // 2 - self.label_text.width() // 2,
                             self.height() // 2 - self.label_text.height() // 2)

    def resizeEvent(self, a0: Qt.QResizeEvent) -> None:
        self.init_background(a0.size().width(), a0.size().height())
        self._resize_label(a0.size().width(), a0.size().height())
