from common.PathObjects import File
from previews.QFilePathObjectPreview import QFilePathObjectPreview
from values.TypeFormatFile import TypeFormatFile


class QMediaFilePreview(QFilePathObjectPreview):
    def __init__(self, x: int, y: int, path_object: File, manager):
        super().__init__(x, y, path_object, manager)
        assert self.path_object.get_type_format() == TypeFormatFile.MEDIA
