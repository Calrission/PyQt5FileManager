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
        self._children = []
        self.resize(w, self.height())
        self.title_txt = title
        self.empty_label = None
        self.title = None
        self.start_list_labels = 0
        self.init_title()
        self.refresh()

    def init_title(self):
        self.title = QLabel(self.title_txt)
        self.title.setParent(self)
        UtilsVisual.set_color_text(self.title, COLOR_TEXT)
        self.title.show()
        self.title.resize(self.width(), self.title.height())
        self.title.setAlignment(Qt.Qt.AlignCenter)
        self.title.move(self.title.x(), 2 * MARGIN_ITEM)
        self._children.append(self.title)
        self.title.show()
        self.start_list_labels = self.title.y() + self.title.height()

    def _get_bottom_max_y(self):
        if len(self._children) == 0:
            return 0, 0
        return max([(i.y(), i.height()) for i in self._children])

    def init_empty_label(self):
        self.empty_label = QLabel("Пусто")
        self.empty_label.setParent(self)
        UtilsVisual.set_color_text(self.empty_label, COLOR_TEXT)
        self.empty_label.resize(self.width(), self.height())
        self.empty_label.setAlignment(Qt.Qt.AlignCenter)
        self.empty_label.move(self.title.x(), self.start_list_labels )
        self._children.append(self.empty_label)

    def add_item(self, item: str):
        if self.empty_label is not None:
            self.hide_empty_label()
        self._items.append(item)
        self._add_new_label(item)

    def add_all_item(self, items: list):
        for item in items:
            self.add_item(item)

    def get_items(self):
        return self._items

    def re_move_labels(self):
        for index, label in enumerate(self._labels):
            prev_y = self._labels[index - 1].y() if index != 0 else self.start_list_labels
            y = 2 * MARGIN_ITEM + prev_y
            label.move(label.x(), y)

    def refresh(self):
        if len(self._items) == 0:
            self.init_empty_label()
        else:
            self.re_move_labels()
            self.hide_empty_label()
        self._update_size()

    def clear(self):
        self._items.clear()
        self.refresh()

    def _add_new_label(self, text: str):
        x = MARGIN_ITEM * 2
        bottom_y, bottom_height = self._get_bottom_max_y()
        y = bottom_y + bottom_height + MARGIN_ITEM * 2
        width = self.width() - MARGIN_ITEM * 4
        new_item = QImageButton(self, text)
        new_item.resize(width, new_item.height())
        new_item.move(x, y)
        new_item.show()
        self._labels.append(new_item)
        self._children.append(new_item)
        self._update_size()

    def _remove_label(self, text: str):
        index = self._items.index(text)
        label = self._labels[index]
        label.deleteLater()
        self._children.remove(label)
        self._labels.remove(label)

    def remove_item(self, item: str):
        self._remove_label(item)
        self._items.remove(item)
        self.refresh()

    def _update_size(self):
        bottom_y, bottom_height = self._get_bottom_max_y()
        h = bottom_y + bottom_height + MARGIN_ITEM * 2
        self.resize(self.width(), h)

    def resizeEvent(self, a0: Qt.QResizeEvent) -> None:
        self.init_background(a0.size().width(), a0.size().height())

    def _clear_labels(self):
        for label in self._labels:
            label.deleteLater()

    def hide_empty_label(self):
        if self.empty_label is not None:
            self.empty_label.deleteLater()
            self._children.remove(self.empty_label)
        self.empty_label = None

    def remove_all_item(self, need_remove):
        for item in need_remove:
            self.remove_item(item)
