from common.PathObjects import File
from widgets.QPathObject import QPathObject
from values.ConstValues import *


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
