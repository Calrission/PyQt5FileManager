from Overlays import QSmartWidget
from PathObjects import PathObject, File, TypeFormatFile


class QPathObjectPreview(QSmartWidget):
    def __init__(self, x: int, y: int, path_object: PathObject, parent):
        super().__init__(x, y, parent)
        self.path_object = path_object

    def initUI(self):
        pass


class QFilePathObjectPreview(QPathObjectPreview):
    def __init__(self, x: int, y: int, path_object: File, parent):
        super().__init__(x, y, path_object, parent)
        self.path_object = path_object


class QMediaFilePreview(QFilePathObjectPreview):
    def __init__(self, x: int, y: int, path_object: File, parent):
        super().__init__(x, y, path_object, parent)
        assert self.path_object.get_type_format() == TypeFormatFile.MEDIA


class QTextFilePreview(QFilePathObjectPreview):
    def __init__(self, x: int, y: int, path_object: File, parent):
        super().__init__(x, y, path_object, parent)
        assert self.path_object.get_type_format() in [TypeFormatFile.TXT, TypeFormatFile.CODE]


class QImagePreview(QMediaFilePreview):
    def __init__(self, x: int, y: int, path_object: File, parent):
        super().__init__(x, y, path_object, parent)


class QAudioPreview(QMediaFilePreview):
    def __init__(self, x: int, y: int, path_object: File, parent):
        super().__init__(x, y, path_object, parent)


class QTxtPreview(QTextFilePreview):
    def __init__(self, x: int, y: int, path_object: File, parent):
        super().__init__(x, y, path_object, parent)


class QCodePreview(QTextFilePreview):
    def __init__(self, x: int, y: int, path_object: File, parent):
        super().__init__(x, y, path_object, parent)