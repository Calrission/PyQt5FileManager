from areas.WindowArea import WindowArea
from managers.DatabaseManager import DatabaseManager
from values.Areas import Areas
from widgets.QCardList import QCardList
from values.ConstValues import MARGIN_ITEM


class LeftWindowArea(WindowArea):
    def __init__(self, window, db_manager: DatabaseManager):
        super().__init__(window, area=Areas.LeftPanel)
        self.db_manager = db_manager

        self.favorites = QCardList(self.window, self.width - MARGIN_ITEM * 2, "Избранное")
        self.favorites.move(self.start_x + MARGIN_ITEM, self.start_y + MARGIN_ITEM)

        self.children.append(self.favorites)
        self._init_content_favorites()

    def _init_content_favorites(self):
        paths = self.db_manager.favorites.get_favorites()
        self.favorites.add_all_item(paths)

    def refresh_favorites(self):
        paths = self.db_manager.favorites.get_favorites()
        now_paths = self.favorites.get_items()
        need_add = [path for path in paths if path not in now_paths]
        need_remove = [path for path in now_paths if path not in paths]
        # self.favorites.remove_all_item(need_remove)
        # self.favorites.add_all_item(need_add)
        for i in need_add:
            self.favorites.add_item(i)
