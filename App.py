from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5 import uic
from ConstValues import *


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setupWindow()
        self.initUI()

    def setupWindow(self):
        self.setGeometry(0, 0, WIDTH, MAX_WIDTH)
        self.setWindowTitle(TITLE)
        self.setMinimumWidth(MIN_WIDTH)
        self.setMaximumWidth(MAX_WIDTH)
        self.setMaximumHeight(MAX_HEIGHT)
        self.setMinimumHeight(MIN_HEIGHT)

    def initUITestMarkup(self):
        tp = QPushButton("TP", self)
        tp.resize(WIDTH_TP, HEIGHT_TP)
        tp.move(START_X_TP, START_Y_TP)

        lp = QPushButton("LP", self)
        lp.resize(WIDTH_LP, HEIGHT_LP)
        lp.move(START_X_LP, START_Y_LP)

        mp = QPushButton("MP", self)
        mp.resize(WIDTH_MP, HEIGHT_MP)
        mp.move(START_X_MP, START_Y_MP)

    def initUI(self):
        pass

