from common.PathObjects import File, PathObject
from previews.QImagePreview import QImagePreview
from previews.QTextPreview import QTextPreview
from values.ConstValues import IMAGE_FORMATS
from values.TypeFormatFile import TypeFormatFile


class PreviewsFactory:
    @staticmethod
    def get_preview_path_object(x, y, parent, path_object: PathObject):
        if isinstance(path_object, File):
            if path_object.get_type_format() == TypeFormatFile.MEDIA:
                return PreviewsFactory.get_preview_media_file(x, y, parent, path_object)
            if path_object.get_type_format() == TypeFormatFile.TXT:
                return QTextPreview(x, y, path_object, parent)

    @staticmethod
    def get_preview_media_file(x, y, parent, file: File):
        if file.format in IMAGE_FORMATS:
            return QImagePreview(x, y, file, parent)
