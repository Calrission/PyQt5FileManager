from PyQt5.QtWidgets import *
from PathObjects import *
from ConstValues import *
from PyQt5.QtCore import Qt
from ImageLoaderPixmap import *
from PyQt5.QtGui import QFont


class QPathObject(QWidget):
    def __init__(self, obj: PathObject, parent=None, icon="files/unknown.png"):
        QWidget.__init__(self, parent=parent)
        self.icon = icon
        self.obj = obj
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, WIDTH_ITEM, HEIGHT_ITEM)
        image = QLabel(self)
        text = QLabel(self)
        text.setAlignment(Qt.AlignHCenter)
        text.setFixedHeight(HEIGHT_TEXT)
        text.setFixedWidth(WIDTH_TEXT)
        text.setFont(QFont('Arial', FONT_SIZE))
        text.setText(self.refactor_text(self.obj.name))
        image.setScaledContents(True)
        image.resize(WIDTH_ICON, HEIGHT_ICON)
        ImageLoaderPixmap.loadToLabel(self.icon, image)
        image.move(WIDTH_ITEM // 2 - WIDTH_ICON // 2, 0)
        image.show()
        text.move(0, HEIGHT_ICON)
        text.show()

    @staticmethod
    def refactor_text(txt: str):
        count_lines = len(txt) // MAX_LINE_TEXT
        lines = [txt[i * MAX_LINE_TEXT: i * MAX_LINE_TEXT + MAX_LINE_TEXT] for i in range(count_lines + 1)]
        if len(lines) > 3:
            lines = lines[:3]
            lines[-1] = lines[-1][:-3] + "..."
        return "\n".join(lines)


class QFile(QPathObject):
    def __init__(self, file: File, parent=None):
        QPathObject.__init__(self, file, parent=parent, icon="files/preview.png")

    def _calc_icon(self):
        pass


class QFolder(QPathObject):
    def __init__(self, folder: Folder, parent=None):
        QPathObject.__init__(self, folder, parent=parent, icon="files/folder.png")

