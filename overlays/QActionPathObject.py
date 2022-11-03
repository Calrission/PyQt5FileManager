from PyQt5.QtWidgets import QWidget
from common.PathObjects import PathObject, File, TypeFormatFile, TypePathObject
from overlays.QActionMenu import QActionMenu
from values.Action import Action


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