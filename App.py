import traceback

from PyQt5 import QtGui, Qt
from PyQt5.QtGui import QMouseEvent, QIcon
from areas.ButtonsAreaWindow import ButtonsAreaWindow
from areas.MainWindowArea import MainWindowArea
from areas.MouseArea import MouseArea
from areas.TabWindowArea import TabWindowArea
from areas.WindowArea import WindowArea
from common.PathObjects import Folder
from common.Tab import Tab
from managers.DatabaseManager import DatabaseManager
from values.Areas import Areas
from values.ConstValues import *
from managers.OverlayManager import QWidgetOverlayManager
from managers.PreviewsManager import PreviewsManager


class Main(PreviewsManager, QWidgetOverlayManager, DatabaseManager):
    def __init__(self):
        DatabaseManager.__init__(self)
        QWidgetOverlayManager.__init__(self)
        PreviewsManager.__init__(self)

        self.setMouseTracking(True)

        self.app = None
        self.tabs = None
        self.left = None
        self.main = None
        self.history_buttons = None

        self.next_h = None
        self.prev_h = None

        self.mouse_listener = None

        self.setupWindow()
        self.setupAreas()

    def excepthook(self, exc_type, exc_value, exc_tb):
        message = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        self.show_error(str(exc_value))
        print(message)

    def setupWindow(self):
        self.setWindowIcon(QIcon('files/icon.png'))
        self.setGeometry(0, 0, WIDTH, HEIGHT)
        self.setWindowTitle(TITLE)
        self.setMinimumWidth(MIN_WIDTH)
        self.setMaximumWidth(MAX_WIDTH)
        self.setMaximumHeight(MAX_HEIGHT)
        self.setMinimumHeight(MIN_HEIGHT)

    def setupAreas(self):
        self.app = WindowArea(window=self, area=Areas.App)
        self.left = WindowArea(window=self, area=Areas.LeftPanel)
        self.main = MainWindowArea(window=self,
                                   preview_manager=self,
                                   on_new_tab=self.on_new_tab)
        self.tabs = TabWindowArea(window=self,
                                  on_add_tab=self.on_add_tab,
                                  on_unselect_tab=self.on_unselect_tab,
                                  on_select_tab=self.on_select_tab,
                                  on_remove_tab=self.on_remove_tab,
                                  on_change_tab=self.on_change_tab,
                                  on_prepare=self.on_prepare,
                                  tabs=self.get_tabs_for_prepare())
        self.history_buttons = ButtonsAreaWindow(window=self,
                                                 click_back_history=self.click_back_history,
                                                 click_next_history=self.click_next_history,
                                                 click_setting=self.click_setting)

        self.mouse_listener = MouseArea([self.tabs, self.left, self.main, self.history_buttons])

        self.tabs.prepare()

    def get_tabs_for_prepare(self):
        opened_tabs = self.open_tabs.get_all_open_tabs()
        if len(opened_tabs) != 0:
            return opened_tabs
        else:
            self.open_tabs.add_open_tab(START_TAB)
            return [START_TAB]

    def on_prepare(self, tabs: list, select_index: int):
        self.on_select_tab(tabs[select_index], select_index)
        self.sync_history_buttons()

    def on_add_tab(self, tab: Tab):
        self.open_tabs.add_open_tab(tab.folder.path)

    def on_remove_tab(self, tab: Tab, index: int):
        self.open_tabs.remove_single_open_tab(tab.folder.path)

    def on_select_tab(self, tab: Tab, index: int):
        self.main.set_tab(tab)
        self.sync_history_buttons()

    def on_new_tab(self, folder: Folder):
        self.tabs.tab_manager.add_new_tab_select(folder.path)

    def on_change_tab(self, last_folder: str, tab: Tab):
        self.open_tabs.update_open_tab(last_folder, tab.folder.path)
        self.sync_history_buttons()

    def on_unselect_tab(self, tab: Tab):
        pass

    def click_back_history(self):
        tab = self.tabs.tab_manager.get_select_tab()
        tab.move_prev_history()
        self.sync_history_buttons()

    def click_next_history(self):
        tab = self.tabs.tab_manager.get_select_tab()
        tab.move_next_history()
        self.sync_history_buttons()

    def click_setting(self):
        pass

    def sync_history_buttons(self):
        select_tab = self.tabs.tab_manager.get_select_tab()
        can_next = select_tab.history.can_next()
        can_prev = select_tab.history.can_prev()
        self.history_buttons.next_h.setEnabled(can_next)
        self.history_buttons.prev_h.setEnabled(can_prev)

    def mousePressEvent(self, event):
        self.mouse_listener.get_area_last_detect_mouse().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.mouse_listener.mouseMoveEvent(event)

    def is_active(self):
        return QWidgetOverlayManager.is_active(self) or PreviewsManager.is_active(self)

    def wheelEvent(self, event):
        if not self.is_active():
            angle = event.angleDelta().y()
            area = self.mouse_listener.get_area_last_detect_mouse()
            if isinstance(area, MainWindowArea):
                px_y = int(angle * ANGLE_WHEEL_TO_PX)
                if (angle < 0 and area.get_need_wheel_down()) or (angle > 0 and area.get_need_wheel_top()):
                    area.delta_change_y_children(px_y)
                    self.tabs.raise_()
                    self.history_buttons.raise_()
            elif isinstance(area, TabWindowArea):
                px_x = int(angle * ANGLE_WHEEL_TO_PX)
                if (angle < 0 and area.get_need_wheel_right()) or (angle > 0 and area.get_need_wheel_left()):
                    area.delta_change_x_children(px_x)
                    self.history_buttons.raise_()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Qt.Key_F5:
            self.main.refresh_content()

