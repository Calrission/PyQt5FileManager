from PyQt5.QtWidgets import QWidget
from common.PathObjects import PathObject, File, TypeFormatFile, TypePathObject, Folder
from managers.DatabaseManager import DatabaseManager
from overlays.QActionMenu import QActionMenu
from values.Action import Action


class QActionPathObject(QActionMenu):
    @staticmethod
    def get_instance(path_object: PathObject, x: int, y: int, parent: QWidget, db_manager: DatabaseManager):
        can_pre_watch = isinstance(path_object, File) and path_object.type == TypePathObject.FILE and \
                        path_object.get_type_format() in [TypeFormatFile.MEDIA, TypeFormatFile.CODE, TypeFormatFile.TXT]
        can_open_new_tab = isinstance(path_object, Folder)
        favorite_action = Action.REMOVE_FAVORITE if db_manager.favorites.check_favorite(path_object.path) else Action.ADD_FAVORITE
        items = [
            Action.OPEN, Action.RENAME, favorite_action, Action.DELETE, Action.INFO
        ]
        if can_pre_watch:
            items.insert(1, Action.PRE_OPEN)
        if can_open_new_tab:
            items.insert(1, Action.OPEN_NEW_TAB)

        return QActionPathObject(path_object, x, y, parent, items)

    def __init__(self, path_object: PathObject, x: int, y: int, parent: QWidget, items: list[Action]):
        super().__init__(x, y, parent, items)
        self.path_object = path_object

    def _click_item_event(self, action: Action):
        self.clickItemEvent(action, self.path_object)