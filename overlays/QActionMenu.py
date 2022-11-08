import math
from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QWidget
from overlays.QOverlay import QOverlay
from values.Action import Action
from values.ConstValues import MARGIN_ITEM_ACTION


class QActionMenu(QOverlay):
    def __init__(self, x: int, y: int, parent: QWidget, items: list[Action]):
        super().__init__(x, y, parent)
        self.items = items
        self.labels = []
        self.clickItemEvent = None

    def initUI(self):
        super().initUI()
        self.refresh()

    def refresh(self):
        self.labels.clear()
        for index, item in enumerate(self.items):
            label = QLabel(item.value)
            label.setParent(self)
            UtilsVisual.set_color_text(self.label, COLOR_TEXT)
            label.adjustSize()
            label.move(MARGIN_ITEM_ACTION, index * 25 + MARGIN_ITEM_ACTION)
            label.show()
            self.labels.append(label)
        w, h = max([i.width() for i in self.labels]) + MARGIN_ITEM_ACTION * 2, len(self.items) * 25 + MARGIN_ITEM_ACTION
        self._init_background(w, h)
        self.resize(w, h)

    def get_action_from_label(self, label: QLabel):
        return self.items[self.labels.index(label)]

    def _get_label_from_y(self, y: int):
        return self.labels[math.floor(y / 25)]

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        label = self._get_label_from_y(event.pos().y())
        if isinstance(label, QLabel):
            action = self.get_action_from_label(label)
            if self.clickItemEvent is not None:
                self._click_item_event(action)

    def _click_item_event(self, action: Action):
        self.clickItemEvent(action)