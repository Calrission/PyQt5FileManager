from PyQt5 import Qt

from areas.WindowArea import WindowArea
from managers.DatabaseManager import DatabaseManager
from managers.OverlayManager import QWidgetOverlayManager
from overlays.QActionFavorite import QActionFavorite
from values.Action import Action
from values.Areas import Areas
from widgets.QCardList import QCardList
from values.ConstValues import MARGIN_ITEM


class LeftWindowArea(WindowArea):
    def __init__(self,
                 window,
                 overlay_manager: QWidgetOverlayManager,
                 db_manager: DatabaseManager,
                 on_open_path_object):
        super().__init__(window, area=Areas.LeftPanel)

        self.db_manager = db_manager
        self.overlay_manager = overlay_manager

        self.on_open_path_object = on_open_path_object

        self.favorites = QCardList(self.window, self.width - MARGIN_ITEM * 2, "Избранное")
        self.favorites.move(self.start_x + MARGIN_ITEM, self.start_y + MARGIN_ITEM)
        self.favorites.click_item = self._click_favorite

        self.children.append(self.favorites)
        self._init_content_favorites()

    def _click_favorite(self, event: Qt.QMouseEvent, path):
        if event.button() == Qt.Qt.LeftButton:
            self.on_open_path_object(path)
        else:
            overlay = QActionFavorite(event.globalX() - self.start_x, event.globalY() - self.start_y, self.window, path)
            overlay.clickItemEvent = self.overlay_action
            self.overlay_manager.add_new_overlay(overlay)
            self.overlay_manager.show_overlay(overlay)

    def overlay_action(self, action: Action, path: str):
        self.overlay_manager.dismiss_all()
        if action == Action.REMOVE_FAVORITE:
            self.db_manager.favorites.remove_favorite(path)
            self.refresh_favorites()

    def _init_content_favorites(self):
        paths = self.db_manager.favorites.get_favorites()
        self.favorites.add_all_item(paths)

    def refresh_favorites(self):
        paths = self.db_manager.favorites.get_favorites()
        now_paths = self.favorites.get_items()
        need_add = [path for path in paths if path not in now_paths]
        need_remove = [path for path in now_paths if path not in paths]
        self.favorites.remove_all_item(need_remove)
        self.favorites.add_all_item(need_add)
