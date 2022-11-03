from common.PathObjects import File
from previews.QPathObjectPreview import QPathObjectPreview


class QFilePathObjectPreview(QPathObjectPreview):
    def __init__(self, x: int, y: int, path_object: File, parent):
        super().__init__(x, y, path_object, parent)
        self.path_object = path_object
