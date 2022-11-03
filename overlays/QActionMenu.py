import math
from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QWidget
from overlays.QOverlay import QOverlay
from values.Action import Action


class QActionMenu(QOverlay):
    def __init__(self, x: int, y: int, parent: QWidget, items: list[Action]):
        super().__init__(x, y, parent)
        self.items = items
        self.labels = []
        self.clickItemEvent = None

    def initUI(self):
        self.refresh()

    def refresh(self):
        self.labels.clear()
        for index, item in enumerate(self.items):
            label = QLabel(item.value)
            label.setParent(self)
            label.setStyleSheet("QLabel { color: rgb(255, 255, 255); }")
            label.adjustSize()
            label.move(5, index * 25 + 5)
            self.labels.append(label)
        self._init_background(self.width(), len(self.items) * 25 + 5)

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