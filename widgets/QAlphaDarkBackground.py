from PyQt5.QtWidgets import QWidget, QLabel
from common.UtilsVisual import UtilsVisual
from values.ConstValues import WIDTH, HEIGHT


class QAlphaDarkBackground(QWidget):
    def __init__(self, alpha=190):
        super().__init__()
        self.background = QLabel(self)
        self.background.resize(WIDTH, HEIGHT)
        self.background.mousePressEvent = self.press_background
        self.click_background = None
        UtilsVisual.set_background_color_label(self.background, (0, 0, 0), WIDTH, HEIGHT, alpha)

    def press_background(self, *args):
        if self.click_background is not None:
            self.click_background()
        self.background.hide()

    def show_background(self):
        self.background.raise_()
        self.background.show()
