from PyQt5 import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel

from common.UtilsVisual import UtilsVisual
from overlays.QOverlay import QOverlay
from values.ConstValues import ALERT_OVERLAY_HEIGHT, ALERT_OVERLAY_WIDTH, COLOR_TEXT


class QActionAlertDialog(QOverlay):
    def __init__(self, message: str, parent: QWidget):
        super().__init__(parent.width() // 2 - ALERT_OVERLAY_WIDTH // 2,
                         parent.height() // 2 - ALERT_OVERLAY_HEIGHT // 2,
                         parent)
        self._positive = None
        self._positive_txt = None
        self.message = message
        self._negative = None
        self._negative_txt = None
        self._label = None

    def initUI(self):
        self.resize(300, 200)
        self._label = QLabel(self.message)
        self._label.setParent(self)
        self._label.setFont(QFont("Arial", 14, QFont.Bold))
        self._label.setWordWrap(True)
        UtilsVisual.set_color_text(self._label, COLOR_TEXT)
        self._label.adjustSize()
        self._label.resize(self.width() - 20, self._label.height())
        self._label.setAlignment(Qt.Qt.AlignHCenter)
        self._label.move(10, 15)

        if self._positive_txt is not None:
            positive = QLabel(self._positive_txt)
            positive.setParent(self)
            positive.setFont(QFont("Arial", 12, QFont.Bold))
            UtilsVisual.set_color_text(positive, COLOR_TEXT)
            positive.show()
            positive.move(self.width() - positive.width() - 20, self.height() - 40)
            if self._positive is not None:
                positive.mousePressEvent = lambda x: self._click_positive()

        if self._negative_txt is not None:
            cancel = QLabel(self._negative_txt)
            cancel.setParent(self)
            cancel.setFont(QFont("Arial", 12, QFont.Bold))
            UtilsVisual.set_color_text(cancel, COLOR_TEXT)
            cancel.move(20, self.height() - 40)
            if self._negative is not None:
                cancel.mousePressEvent = lambda x: self._click_negative()
        super().initUI()

    def _click_positive(self):
        self._positive()

    def _click_negative(self):
        self._negative()

    def set_negative(self, txt: str, click):
        self._negative_txt = txt
        self._negative = click

    def set_positive(self, txt: str, click):
        self._positive_txt = txt
        self._positive = click