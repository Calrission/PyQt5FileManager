from PyQt5.QtWidgets import QWidget
from enum import Enum
from ConstValues import *


class Areas(Enum):
    TabPanel = (START_X_TP, END_X_TP, START_Y_TP, END_Y_TP)
    MainPanel = (START_X_MP, END_X_MP, START_Y_MP, END_Y_MP)
    LeftPanel = (START_X_LP, END_X_LP, START_Y_LP, END_Y_LP)


class WindowArea:
    def __init__(self, window: QWidget,
                 start_x: int = None, end_x: int = None,
                 start_y: int = None, end_y: int = None,
                 area: Areas = None):
        if area is None:
            self.end_y = end_y
            self.start_y = start_y
            self.end_x = end_x
            self.start_x = start_x
            self.window = window
        else:
            self.__init__(window, area.value[0], area.value[1], area.value[2], area.value[3])

    def add_widget(self, widget: QWidget, width: int = None,
                   height: int = None, x: int = None, y: int = None):
        width = widget.width() if width is None else width
        height = widget.height() if height is None else height
        x = widget.x() if x is None else x
        y = widget.y() if y is None else y

        widget.setParent(self.window)
        widget.resize(width, height)
        widget.move(x, y)
