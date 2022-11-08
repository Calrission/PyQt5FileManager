from PyQt5 import Qt
from PyQt5.QtWidgets import QLabel

from common.UtilsVisual import UtilsVisual
from widgets.QImageBackground import QImageBackground
from values.ConstValues import MARGIN_ITEM, COLOR_TEXT
from widgets.QImageButton import QImageButton


class QCardList(QImageBackground):
    def __init__(self, parent, w: int, title: str, items: list = None):
        super().__init__(parent, "files/back_tag_select")
        self._items = items if items is not None else []
        self._labels = []
        self.resize(w, self.height())
        if len(self._items) != 0:
            self.refresh()
        self.title_txt = title
        self.title = None
        self.init_title()

    def init_title(self):
        self.title = QLabel(self.title_txt)
        self.title.setParent(self)
        UtilsVisual.set_color_text(self.title, COLOR_TEXT)
        self.title.show()
        self.title.resize(self.width(), self.title.height())
        self.title.setAlignment(Qt.Qt.AlignCenter)
        self.title.move(self.title.x(), MARGIN_ITEM)

    def add_item(self, item: str):
        self._items.append(item)
        self._add_new_label(item)

    def refresh(self):
        self._clear_labels()
        for item in self._items:
            self._add_new_label(item)

    def clear(self):
        self._items.clear()
        self._clear_labels()

    def _add_new_label(self, text: str):
        x = MARGIN_ITEM * 2
        y = self._labels[-1].y() + self._labels[-1].height() + MARGIN_ITEM * 2 if len(self._labels) > 0 else MARGIN_ITEM + self.title.y() + self.title.height()
        width = self.width() - MARGIN_ITEM * 4
        new_item = QImageButton(self, text)
        new_item.resize(width, new_item.height())
        new_item.move(x, y)
        self._labels.append(new_item)
        self._update_size()

    def _remove_label(self, text: str):
        index = self._items.index(text)
        self._labels.remove(self._labels[index])

    def remove_item(self, item: str):
        self._items.remove(item)
        self._remove_label(item)

    def _update_size(self):
        h = self._labels[-1].y() + self._labels[-1].height() + MARGIN_ITEM * 2
        self.resize(self.width(), h)

    def resizeEvent(self, a0: Qt.QResizeEvent) -> None:
        self.init_background(a0.size().width(), a0.size().height())

    def _clear_labels(self):
        for label in self._labels:
            label.deleteLater()