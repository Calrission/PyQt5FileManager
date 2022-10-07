from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5 import uic
from ConstValues import *
from WindowArea import *
from PathObjects import *
from Tab import *


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.tabs = None
        self.left = None
        self.main = None

        self.setupWindow()
        self.setupAreas()
        self.initUI()

    def setupWindow(self):
        self.setGeometry(0, 0, WIDTH, MAX_WIDTH)
        self.setWindowTitle(TITLE)
        self.setMinimumWidth(MIN_WIDTH)
        self.setMaximumWidth(MAX_WIDTH)
        self.setMaximumHeight(MAX_HEIGHT)
        self.setMinimumHeight(MIN_HEIGHT)

    def setupAreas(self):
        self.tabs = TabWindowArea(window=self, area=Areas.TabPanel,
                                  on_add_tab=self.on_add_tab,
                                  on_unselect_tab=self.on_unselect_tab,
                                  on_select_tab=self.on_select_tab,
                                  on_remove_tab=self.on_remove_tab)
        self.left = WindowArea(window=self, area=Areas.LeftPanel)
        self.main = WindowArea(window=self, area=Areas.MainPanel)

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

    def on_add_tab(self, tab: Tab):
        print(f"add tab {tab}")

    def on_remove_tab(self, tab: Tab):
        print(f"remove tab {tab}")

    def on_select_tab(self, tab: Tab):
        print(f"select tab {tab}")

    def on_unselect_tab(self, tab: Tab):
        print(f"unselect tab {tab}")

    def initUI(self):
        self.tabs.tab_manager.add_new_tab("/home/artemii/Загрузки")
        self.tabs.tab_manager.add_new_tab("/home/artemii")
