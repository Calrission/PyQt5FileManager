import traceback

from PyQt5 import QtGui

from Overlays import QOverlay
from WindowArea import *
from Tab import *
from MouseAreaListener import MouseAreaListener


class Main(QWidgetOverlayManager):
    def __init__(self):
        super().__init__()
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
        self.initUI()

    def excepthook(self, exc_type, exc_value, exc_tb):
        # message = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        # error_overlay = QOverlay()
        # self.add_new_overlay(error_overlay, self.manager.max() + 1)
        pass

    def setupWindow(self):
        self.setWindowIcon(QtGui.QIcon('files/icon.png'))
        self.setGeometry(0, 0, WIDTH, HEIGHT)
        self.setWindowTitle(TITLE)
        self.setMinimumWidth(MIN_WIDTH)
        self.setMaximumWidth(MAX_WIDTH)
        self.setMaximumHeight(MAX_HEIGHT)
        self.setMinimumHeight(MIN_HEIGHT)

    def setupAreas(self):
        self.app = WindowArea(window=self, area=Areas.App)
        self.left = WindowArea(window=self, area=Areas.LeftPanel)
        self.main = MainWindowArea(window=self)
        self.tabs = TabWindowArea(window=self,
                                  on_add_tab=self.on_add_tab,
                                  on_unselect_tab=self.on_unselect_tab,
                                  on_select_tab=self.on_select_tab,
                                  on_remove_tab=self.on_remove_tab,
                                  on_change_tab=self.on_change_tab)
        self.history_buttons = ButtonsAreaWindow(window=self,
                                                 click_back_history=self.click_back_history,
                                                 click_next_history=self.click_next_history,
                                                 click_setting=self.click_setting)

        self.mouse_listener = MouseAreaListener([self.tabs, self.left, self.main])

    def on_add_tab(self, tab: Tab):
        pass

    def on_remove_tab(self, tab: Tab):
        pass

    def on_select_tab(self, tab: Tab):
        self.main.set_tab(tab)
        self.sync_history_buttons()

    def on_change_tab(self, tab: Tab):
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

    def initUI(self):
        self.tabs.tab_manager.add_new_tab(START_TAB)
        self.sync_history_buttons()

    def mouseMoveEvent(self, event):
        self.mouse_listener.mouseMoveEvent(event)

    def wheelEvent(self, event):
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
