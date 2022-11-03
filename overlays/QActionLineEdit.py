from PyQt5.QtWidgets import QWidget, QLineEdit
from overlays.QActionAlertDialog import QActionAlertDialog


class QActionLineEdit(QActionAlertDialog):
    def __init__(self, parent: QWidget, message: str, default_text=""):
        super().__init__(message, parent)
        self.default_text = default_text
        self.new_name = None

    def initUI(self):
        super().initUI()
        y = self._label.y() + self._label.height() + 20
        self.new_name = QLineEdit(self)
        self.new_name.setText(self.default_text)
        self.new_name.resize(self.width() - 20, 40)
        self.new_name.move(10, y)

    def _click_positive(self):
        self._positive(self.new_name.text())

    def _click_negative(self):
        self._negative()