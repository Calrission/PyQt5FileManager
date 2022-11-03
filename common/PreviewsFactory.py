from common.PathObjects import File, PathObject
from previews.QImagePreview import QImagePreview
from values.ConstValues import IMAGE_FORMATS


class PreviewsFactory:
    @staticmethod
    def get_preview_path_object(x, y, parent, path_object: PathObject):
        if isinstance(path_object, File):
            return PreviewsFactory.get_preview_media_file(x, y, parent, path_object)

    @staticmethod
    def get_preview_media_file(x, y, parent, file: File):
        if file.format in IMAGE_FORMATS:
            return QImagePreview(x, y, file, parent)
