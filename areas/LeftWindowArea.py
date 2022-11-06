from areas.WindowArea import WindowArea
from managers.DatabaseManager import DatabaseManager
from values.Areas import Areas


class LeftWindowArea(WindowArea):
    def __init__(self, window, db_manager: DatabaseManager):
        super().__init__(window, area=Areas.LeftPanel)
        self.db_manager = db_manager

    