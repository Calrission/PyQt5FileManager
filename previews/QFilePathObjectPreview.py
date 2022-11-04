from common.PathObjects import File
from managers.PreviewsManager import PreviewsManager
from previews.QPathObjectPreview import QPathObjectPreview


class QFilePathObjectPreview(QPathObjectPreview):
    def __init__(self, x: int, y: int, path_object: File, manager: PreviewsManager):
        super().__init__(x, y, path_object, manager)
        self.path_object = path_object
