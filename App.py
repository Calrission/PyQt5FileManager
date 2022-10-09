from PyQt5.QtGui import QMoveEvent
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5 import uic
from ConstValues import *
from WindowArea import *
from PathObjects import *
from Tab import *
from MouseAreaListener import MouseAreaListener


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

        self.tabs = None
        self.left = None
        self.main = None

        self.next_h = None
        self.prev_h = None

        self.mouse_listener = None

        self.setupWindow()
        self.setupAreas()
        self.initUI()

    def setupWindow(self):
        self.setGeometry(0, 0, WIDTH, HEIGHT)
        self.setWindowTitle(TITLE)
        self.setMinimumWidth(MIN_WIDTH)
        self.setMaximumWidth(MAX_WIDTH)
        self.setMaximumHeight(MAX_HEIGHT)
        self.setMinimumHeight(MIN_HEIGHT)

    def setupAreas(self):
        self.tabs = TabWindowArea(window=self,
                                  on_add_tab=self.on_add_tab,
                                  on_unselect_tab=self.on_unselect_tab,
                                  on_select_tab=self.on_select_tab,
                                  on_remove_tab=self.on_remove_tab,
                                  on_change_tab=self.on_change_tab)
        self.left = WindowArea(window=self, area=Areas.LeftPanel)
        self.main = MainWindowArea(window=self)

        self.mouse_listener = MouseAreaListener([self.tabs, self.left, self.main])

    def initUITestMarkup(self):
        tp = QPushButton("TP")
        tp.resize(WIDTH_TP, HEIGHT_TP)
        tp.move(START_X_TP, START_Y_TP)
        self.tabs.add_widget(tp)

        lp = QPushButton("LP")
        lp.resize(WIDTH_LP, HEIGHT_LP)
        lp.move(START_X_LP, START_Y_LP)
        self.left.add_widget(lp)

        mp = QPushButton("MP")
        mp.resize(WIDTH_MP, HEIGHT_MP)
        mp.move(START_X_MP, START_Y_MP)
        self.main.add_widget(mp)

    def initTestMainArea(self):
        self.initUITestMarkup()
        lst = [QPushButton(f"{i + 1}") for i in range(90)]
        [i.resize(WIDTH_ITEM, HEIGHT_ITEM) for i in lst]
        [self.main.add_item(i) for i in lst]

    def on_add_tab(self, tab: Tab):
        print(f"add tab {tab}")

    def on_remove_tab(self, tab: Tab):
        print(f"remove tab {tab}")

    def on_select_tab(self, tab: Tab):
        print(f"select tab {tab}")
        self.main.set_tab(tab)

    def on_change_tab(self, tab: Tab):
        self.sync_history_buttons()

    def on_unselect_tab(self, tab: Tab):
        print(f"unselect tab {tab}")

    def add_history_buttons(self):
        self.next_h = QPushButton(">", self)
        self.next_h.resize(WIDTH_HISTORY_BUTTON, HEIGHT_HISTORY_BUTTON)
        self.next_h.move(START_X_BUTTON_HISTORY + WIDTH_HISTORY_BUTTON + MARGIN_BUTTON_HISTORY, START_Y_BUTTON_HISTORY)
        self.prev_h = QPushButton("<", self)
        self.prev_h.move(START_X_BUTTON_HISTORY, START_Y_BUTTON_HISTORY)
        self.prev_h.clicked.connect(self.click_back_history)
        self.next_h.clicked.connect(self.click_next_history)
        self.prev_h.resize(WIDTH_HISTORY_BUTTON, HEIGHT_HISTORY_BUTTON)

    def click_back_history(self):
        tab = self.tabs.tab_manager.get_select_tab()
        tab.move_prev_history()
        self.sync_history_buttons()

    def click_next_history(self):
        tab = self.tabs.tab_manager.get_select_tab()
        tab.move_next_history()
        self.sync_history_buttons()

    def sync_history_buttons(self):
        select_tab = self.tabs.tab_manager.get_select_tab()
        can_next = select_tab.history.can_next()
        can_prev = select_tab.history.can_prev()
        self.next_h.setEnabled(can_next)
        self.prev_h.setEnabled(can_prev)

    def initUI(self):
        self.tabs.tab_manager.add_new_tab("/home/artemii/Загрузки")
        self.tabs.tab_manager.add_new_tab("/home/artemii")
        self.add_history_buttons()
        self.sync_history_buttons()

    def mouseMoveEvent(self, event):
        self.mouse_listener.mouseMoveEvent(event)

    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        area = self.mouse_listener.get_area_last_detect_mouse()
        if isinstance(area, MainWindowArea):
            px_y = int(angle * ANGLE_WHEEL_TO_PX)
            if (angle < 0 and area.get_need_wheel_down()) or (angle > 0 and area.get_need_wheel_top()):
                print(f"Прокрутка контента по вертикали на {px_y}")
                area.delta_change_y_children(px_y)
