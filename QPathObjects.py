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
        ImageLoaderPixmap.load_file_to_label(self.icon, self.image)

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
        QPathObject.__init__(self, file, parent=parent, icon="files/txt.png")
        self._calc_icon()

    def _calc_icon(self):
        format_ = self.obj.format
        if format_ == "":
            self.icon = "files/shellscript.png"
        if format_ in TXT_FORMATS:
            self.icon = "files/txt.png"
        elif format_ in VIDEO_FORMATS:
            self.icon = "files/video.png"
        elif format_ in ARCHIVE_FORMATS:
            self.icon = "files/archive.png"
        elif format_ in PYTHON_FORMATS:
            self.icon = "files/python.png"
        elif format_ in PYTHON_BYTECODE_FORMATS:
            self.icon = "files/python-bytecode.png"
        elif format_ in WORD_FORMATS:
            self.icon = "files/word.png"
        elif format_ in EXCEL_FORMATS:
            self.icon = "files/excel.png"
        elif format_ in QT_UI_FORMATS:
            self.icon = "files/qt-ui.png"
        elif format_ == POWERPOINT_FORMATS:
            self.icon = "files/powerpoint.png"
        elif format_ in AUDIO_FORMATS:
            self.icon = "files/audio.png"
        elif format_ in APK_FORMATS:
            self.icon = "files/apk.png"
        elif format_ in PDF_FORMATS:
            self.icon = "files/pdf.png"
        elif format_ in JAR_FORMATS:
            self.icon = "files/jar.png"
        elif format_ in JAVA_FORMATS:
            self.icon = "files/java.png"
        elif format_ in TORRENT_FORMATS:
            self.icon = "files/torrent.png"
        elif format_ in IMAGE_FORMATS:
            self.icon = self.obj.path
        self._initIcon()


class QFolder(QPathObject):
    def __init__(self, folder: Folder, parent=None):
        QPathObject.__init__(self, folder, parent=parent, icon="files/folder.png")

