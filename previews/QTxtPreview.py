from common.PathObjects import File
from previews.QTextFilePreview import QTextFilePreview


class QTxtPreview(QTextFilePreview):
    def __init__(self, x: int, y: int, path_object: File, parent):
        super().__init__(x, y, path_object, parent)