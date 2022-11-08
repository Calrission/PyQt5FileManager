from areas.WindowArea import WindowArea
from managers.DatabaseManager import DatabaseManager
from values.Areas import Areas
from widgets.QCardList import QCardList
from values.ConstValues import MARGIN_ITEM, QCARDLIST_DEFAULT_HEIGHT


class LeftWindowArea(WindowArea):
    def __init__(self, window, db_manager: DatabaseManager):
        super().__init__(window, area=Areas.LeftPanel)
        self.db_manager = db_manager

        test = QCardList(self.window, self.width - MARGIN_ITEM * 2)
        test.move(self.start_x + MARGIN_ITEM, self.start_y + MARGIN_ITEM)
        test.add_item("Test")
        test.add_item("Test")


    