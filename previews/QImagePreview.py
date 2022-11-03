from common.PathObjects import File
from common.UtilsVisual import UtilsVisual
from previews.QMediaFilePreview import QMediaFilePreview
from values.ConstValues import IMAGE_FORMATS, MARGIN_ITEM
from widgets.QImageView import QImageView


class QImagePreview(QMediaFilePreview):
    def __init__(self, x: int, y: int, path_object: File, parent):
        super().__init__(x, y, path_object, parent)
        assert self.path_object.check_type_format(IMAGE_FORMATS)
        self.image = None

    def _set_w_h_image(self):
        main_w, main_h = self.parent().width() - self.x - MARGIN_ITEM, self.parent().height() - self.y - MARGIN_ITEM
        w, h = UtilsVisual.get_w_h_image(self.path_object.path)
        scale = min([main_w / w, main_h / h])
        self.image.resize(int(w * scale), int(h * scale))

    def initUI(self):
        self.image = QImageView(self, self.path_object.path)
        self._set_w_h_image()
