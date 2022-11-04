from common.PathObjects import File
from common.UtilsVisual import UtilsVisual
from previews.QMediaFilePreview import QMediaFilePreview
from values.ConstValues import IMAGE_FORMATS, IMAGE_PREVIEW_HEIGHT
from widgets.QImageView import QImageView


class QImagePreview(QMediaFilePreview):
    def __init__(self, x: int, y: int, path_object: File, manager):
        super().__init__(x, y, path_object, manager)
        assert self.path_object.check_type_format(IMAGE_FORMATS)
        self.image = None

    def _set_w_h_content(self):
        w, h = UtilsVisual.get_w_h_image(self.path_object.path)
        scale = IMAGE_PREVIEW_HEIGHT / h
        new_w, new_h = int(w * scale), int(h * scale)
        self.image.resize(new_w, new_h)

    def initUI(self):
        self.image = QImageView(self, self.path_object.path)
        super().initUI()
