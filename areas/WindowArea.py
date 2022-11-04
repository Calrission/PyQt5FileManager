from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QLabel
from common.UtilsVisual import UtilsVisual
from values.Areas import Areas
from values.ConstValues import COLOR_BACKGROUND_DEFAULT, HEIGHT, WIDTH


class WindowArea:
    def __init__(self, window,
                 start_x: int = None, end_x: int = None,
                 start_y: int = None, end_y: int = None,
                 width: int = None, height: int = None,
                 color_background: tuple = COLOR_BACKGROUND_DEFAULT,
                 area: Areas = None):
        if area is None:
            self.end_y = end_y
            self.start_y = start_y
            self.end_x = end_x
            self.start_x = start_x
            self.width = width
            self.height = height
            self.window = window
            self.color_background = color_background
        else:
            WindowArea.__init__(self, window=window,
                                start_x=area.value[0], end_x=area.value[1],
                                start_y=area.value[2], end_y=area.value[3],
                                width=area.value[4], height=area.value[5],
                                color_background=area.value[6])

        self.children: list[QWidget] = []

        self._delta_wheel_x = 0
        self._delta_wheel_y = 0

        self.background = QLabel()
        self.background.resize(self.width, self.height)
        self._add_widget(self.background, self.start_x, self.start_y)
        self.set_color_background_rgb(self.color_background)

    def add_widget(self, widget: QWidget, x: int = None, y: int = None):
        widget = self._add_widget(widget, x, y)
        self.children.append(widget)
        return widget

    def raise_(self):
        self.background.raise_()
        [i.raise_() for i in self.children]

    def _add_widget(self, widget: QWidget, x: int = None, y: int = None):
        x = widget.x() if x is None else x
        y = widget.y() if y is None else y
        widget.setMouseTracking(True)
        widget.setParent(self.window)
        widget.move(x, y)
        widget.show()
        return widget

    def get_bottom_widget(self):
        max_y = -1
        bottom_widget = None
        for widget in self.children:
            if widget.y() > max_y:
                bottom_widget = widget
                max_y = widget.y()
        return bottom_widget

    def get_top_widget(self):
        min_y = HEIGHT + 1
        top_widget = None
        for widget in self.children:
            if widget.y() < min_y:
                top_widget = widget
                min_y = widget.y()
        return top_widget

    def get_left_widget(self):
        min_x = WIDTH + 1
        left_widget = None
        for widget in self.children:
            if widget.x() < min_x:
                left_widget = widget
                min_x = widget.x()
        return left_widget

    def get_right_widget(self):
        max_x = -1
        right_widget = None
        for widget in self.children:
            if widget.x() > max_x:
                right_widget = widget
                max_x = widget.x()
        return right_widget

    def get_need_wheel_left(self):
        left_widget = self.get_left_widget()
        return left_widget.x() < self.start_x

    def get_need_wheel_right(self):
        right_widget = self.get_right_widget()
        return right_widget.x() + right_widget.width() > self.end_x

    def get_need_wheel_down(self):
        bottom_widget = self.get_bottom_widget()
        return bottom_widget.y() + bottom_widget.height() > HEIGHT

    def get_need_wheel_top(self):
        top_widget = self.get_top_widget()
        return top_widget.y() < self.start_y

    def delta_change_y_children(self, delta_y: int):
        self._delta_wheel_y += delta_y
        for widget in self.children:
            widget.move(widget.x(), widget.y() + delta_y)

    def delta_change_x_children(self, delta_x: int):
        self._delta_wheel_x += delta_x
        for widget in self.children:
            widget.move(widget.x() + delta_x, widget.y())

    def delta_wheel_move(self):
        for widget in self.children:
            widget.move(widget.x() + self._delta_wheel_x, widget.y() + self._delta_wheel_y)

    def deleteLaterWidget(self, widget: QWidget):
        widget.deleteLater()
        if widget in self.children:
            self.children.remove(widget)

    def __str__(self):
        return self.__class__.__name__

    def set_color_background_rgb(self, color: tuple):
        UtilsVisual.set_background_color_label(self.background, color)

    def mousePressEvent(self, event: QMouseEvent):
        print(f"click to {self.__class__.__name__}")