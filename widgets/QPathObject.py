from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel
from common.PathObjects import PathObject
from common.UtilsVisual import UtilsVisual
from values.ConstValues import WIDTH_ICON, HEIGHT_ICON, WIDTH_ITEM, HEIGHT_ITEM, MAX_LINE_TEXT, FONT_SIZE, COLOR_TEXT, \
    WIDTH_TEXT, HEIGHT_TEXT


class QPathObject(QWidget):
    def __init__(self, obj: PathObject, parent=None, icon="files/unknown.png"):
        QWidget.__init__(self, parent=parent)
        self.icon = icon
        self.obj = obj
        self.image = None
        self.text = None
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, WIDTH_ITEM, HEIGHT_ITEM)
        self.image = QLabel(self)
        self.text = QLabel(self)
        self.text.setAlignment(Qt.AlignHCenter)
        self.text.setFixedHeight(HEIGHT_TEXT)
        self.text.setFixedWidth(WIDTH_TEXT)
        self.text.setFont(QFont('Arial', FONT_SIZE))
        values = ", ".join([str(i) for i in COLOR_TEXT])
        self.text.setStyleSheet("QLabel { color: rgb("+values+"); }")
        self.text.setText(self.refactor_text(self.obj.name))
        self.image.setScaledContents(True)
        self.image.resize(WIDTH_ICON, HEIGHT_ICON)
        self.image.move(WIDTH_ITEM // 2 - WIDTH_ICON // 2, 0)
        self.image.show()
        self.text.move(0, HEIGHT_ICON)
        self.text.show()
        self._initIcon()

    def _initIcon(self):
        UtilsVisual.load_file_to_label(self.icon, self.image)

    @staticmethod
    def refactor_text(txt: str):
        count_lines = len(txt) // MAX_LINE_TEXT
        lines = [txt[i * MAX_LINE_TEXT: i * MAX_LINE_TEXT + MAX_LINE_TEXT] for i in range(count_lines + 1)]
        if len(lines) > 3:
            lines = lines[:3]
            lines[-1] = lines[-1][:-3] + "..."
        return "\n".join(lines)