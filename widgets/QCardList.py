from PyQt5 import Qt
from PyQt5.QtWidgets import QLabel

from widgets.QImageBackground import QImageBackground
from values.ConstValues import MARGIN_ITEM, COLOR_TEXT
from widgets.QImageButton import QImageButton


class QCardList(QImageBackground):
    def __init__(self, parent, items: list = None):
        super().__init__(parent, "files/back_tag_select")
        self._items = items if items is not None else []
        self._labels = []
        self.resize(self.width(), self.height())
        if len(self._items) != 0:
            self.refresh()

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
        y = self._labels[-1].y() + self._labels[-1].height() + MARGIN_ITEM * 2 if len(self._labels) > 0 else MARGIN_ITEM * 2
        width = self.width() - MARGIN_ITEM * 4
        new_item = QImageButton(self, text)
        new_item.resize(width, new_item.height())
        new_item.move(x, y)
        self._labels.append(new_item)

    def _remove_label(self, text: str):
        index = self._items.index(text)
        self._labels.remove(self._labels[index])

    def remove_item(self, item: str):
        self._items.remove(item)
        self._remove_label(item)

    def resizeEvent(self, a0: Qt.QResizeEvent) -> None:
        self.init_background(a0.size().width(), a0.size().height())

    def _clear_labels(self):
        for label in self._labels:
            label.deleteLater()
