from Overlays import QSmartWidget
from PathObjects import PathObject, File, TypeFormatFile
from ConstValues import *
from QSwitchImageButton import QImageView
from UtilsVisual import UtilsVisual


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


class QAudioPreview(QMediaFilePreview):
    def __init__(self, x: int, y: int, path_object: File, parent):
        super().__init__(x, y, path_object, parent)


class QTxtPreview(QTextFilePreview):
    def __init__(self, x: int, y: int, path_object: File, parent):
        super().__init__(x, y, path_object, parent)


class QCodePreview(QTextFilePreview):
    def __init__(self, x: int, y: int, path_object: File, parent):
        super().__init__(x, y, path_object, parent)


class PreviewsManager:
    def __init__(self):
        self.active_preview = None

    def show_preview(self, preview: QPathObjectPreview):
        if self.active_preview is not None:
            self.dismiss_active_preview()

        self.active_preview = preview
        preview.show()

    def dismiss_active_preview(self):
        if self.active_preview is not None:
            self.active_preview.deleteLater()
            self.active_preview = None


class PreviewsFactory:
    @staticmethod
    def get_preview_path_object(x, y, parent, path_object: PathObject):
        if isinstance(path_object, File):
            return PreviewsFactory.get_preview_media_file(x, y, parent, path_object)

    @staticmethod
    def get_preview_media_file(x, y, parent, file: File):
        if file.format in IMAGE_FORMATS:
            return QImagePreview(x, y, file, parent)
