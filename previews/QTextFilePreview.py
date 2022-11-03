from common.PathObjects import File
from previews.QFilePathObjectPreview import QFilePathObjectPreview
from values.TypeFormatFile import TypeFormatFile


class QTextFilePreview(QFilePathObjectPreview):
    def __init__(self, x: int, y: int, path_object: File, parent):
        super().__init__(x, y, path_object, parent)
        assert self.path_object.get_type_format() in [TypeFormatFile.TXT, TypeFormatFile.CODE]
