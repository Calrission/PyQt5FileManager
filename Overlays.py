import math
from enum import Enum

from PyQt5 import QtGui, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PathObjects import PathObject, TypePathObject, File, TypeFormatFile
from QSwitchImageButton import QImageView
from ConstValues import DELETE_OVERLAY_WIDTH, DELETE_OVERLAY_HEIGHT


class QOverlay(QWidget):
    def __init__(self, x: int, y: int, parent: QWidget):
        self.x = x
        self.y = y
        self.image_background = None
        super().__init__(parent)

    def _calc_x_y(self, x, y):
        new_x = x if x + self.width() <= self.parent().width() else x - self.width()
        new_y = y if y + self.height() <= self.parent().height() else y - self.height()
        self.x, self.y = new_x, new_y

    def move_calc_x_y(self):
        self._calc_x_y(self.x, self.y)
        self.move(self.x, self.y)

    def show(self) -> None:
        self.initUI()
        self.move(self.x, self.y)
        self.raise_()
        super().show()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        self.move_calc_x_y()

    def initUI(self):
        pass

    def _init_background(self, w: int, h: int):
        self.image_background = QImageView(self, path="files/back_tag_select.png")
        self.image_background.resize(w, h)
        self.image_background.lower()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x=}, {self.y=})"


class Action(Enum):
    OPEN = "Открыть"
    RENAME = "Переименовать"
    DELETE = "Удалить"
    PRE_OPEN = "Предпросмотр"
    INFO = "Свойства"
    CREATE_FOLDER = "Создать папку"
    CREATE_FILE = "Создать файл"


class Result(Enum):
    OK = "ok"
    CANCEL = "cancel"


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
            label.setStyleSheet("QLabel { color: rgb(255, 255, 255); }")
            label.adjustSize()
            label.move(5, index * 25 + 5)
            self.labels.append(label)
        self._init_background(self.width(), len(self.items) * 25 + 5)

    def get_action_from_label(self, label: QLabel):
        return self.items[self.labels.index(label)]

    def _get_label_from_y(self, y: int):
        return self.labels[math.ceil(y / 30)]

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        label = self._get_label_from_y(event.pos().y())
        if isinstance(label, QLabel):
            action = self.get_action_from_label(label)
            if self.clickItemEvent is not None:
                self._click_item_event(action)

    def _click_item_event(self, action: Action):
        self.clickItemEvent(action)


class QActionPathObject(QActionMenu):
    @staticmethod
    def get_instance(path_object: PathObject, x: int, y: int, parent: QWidget):
        can_pre_watch = isinstance(path_object, File) and path_object.type == TypePathObject.FILE and \
                        path_object.get_type_format() in [TypeFormatFile.MEDIA, TypeFormatFile.CODE, TypeFormatFile.TXT]
        items = [
            Action.OPEN, Action.RENAME, Action.DELETE, Action.INFO
        ]
        if can_pre_watch:
            items.insert(1, Action.PRE_OPEN)
        return QActionPathObject(path_object, x, y, parent, items)

    def __init__(self, path_object: PathObject, x: int, y: int, parent: QWidget, items: list[Action]):
        super().__init__(x, y, parent, items)
        self.path_object = path_object

    def _click_item_event(self, action: Action):
        self.clickItemEvent(action, self.path_object)


class QActionDeletePathObject(QOverlay):

    def __init__(self, path_object: PathObject, parent: QWidget):
        super().__init__(parent.width() // 2 - DELETE_OVERLAY_WIDTH // 2,
                         parent.height() // 2 - DELETE_OVERLAY_HEIGHT // 2,
                         parent)
        self.path_object = path_object
        self.ok = None
        self.cancel = None

    def initUI(self):
        self.resize(300, 200)
        txt = f"Вы действительно хотите удалить " \
              f"{'папку' if self.path_object.type == TypePathObject.FOLDER else 'файл' if self.path_object.type == TypePathObject.FILE else ''} \"{self.path_object.name}\"?"
        label = QLabel(txt)
        label.setParent(self)
        label.setFont(QFont("Arial", 14, QFont.Bold))
        label.setWordWrap(True)
        label.setStyleSheet("QLabel { color: rgb(255, 255, 255); }")
        label.resize(self.width() - 20, self.height() - 60)
        label.setAlignment(Qt.Qt.AlignHCenter)
        label.move(10, 15)

        ok = QLabel("Да")
        ok.setParent(self)
        ok.move(self.width() - 40, self.height() - 40)
        ok.setFont(QFont("Arial", 12, QFont.Bold))
        ok.setStyleSheet("QLabel { color: rgb(255, 255, 255); }")
        if self.ok is not None:
            ok.mousePressEvent = lambda x: self.ok(self.path_object)

        cancel = QLabel("Отмена")
        cancel.setParent(self)
        cancel.move(20, self.height() - 40)
        cancel.setFont(QFont("Arial", 12, QFont.Bold))
        cancel.setStyleSheet("QLabel { color: rgb(255, 255, 255); }")
        if self.cancel is not None:
            cancel.mousePressEvent = lambda x: self.cancel(self.path_object)

        self._init_background(self.width(), self.height())
