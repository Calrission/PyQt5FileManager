
from PyQt5.QtWidgets import QWidget
from common.Tab import Tab
from overlays.QActionMenu import QActionMenu
from values.Action import Action


class QActionTab(QActionMenu):
    @staticmethod
    def get_instance(tab: Tab, x: int, y: int, parent: QWidget):
        items = [Action.CLOSE_TAB]
        return QActionTab(tab, x, y, parent, items)

    def __init__(self, tab: Tab, x: int, y: int, parent: QWidget, items: list[Action]):
        super().__init__(x, y, parent, items)
        self.tab = tab

    def _click_item_event(self, action: Action):
        self.clickItemEvent(action, self.tab)