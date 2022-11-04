from common.PathObjects import File
from managers.PreviewsManager import PreviewsManager
from previews.QFilePathObjectPreview import QFilePathObjectPreview
from values.TypeFormatFile import TypeFormatFile
from values.ConstValues import TEXT_PREVIEW_WIDTH, TEXT_PREVIEW_HEIGHT
from PyQt5.QtWidgets import QPlainTextEdit


class QTextPreview(QFilePathObjectPreview):
    def __init__(self, x: int, y: int, path_object: File, manager: PreviewsManager):
        super().__init__(x, y, path_object, manager)
        assert self.path_object.get_type_format() in [TypeFormatFile.TXT, TypeFormatFile.CODE]
        self.text = None

    def initUI(self):
        self.text = QPlainTextEdit(self)
        self.text.setReadOnly(True)
        try:
            with open(self.path_object.path, "r", encoding="utf-8") as f:
                self.text.setPlainText(f.read())
        except Exception:
            self.manager.dismiss_active_preview()
        super().initUI()

    def _set_w_h_content(self):
        self.text.resize(TEXT_PREVIEW_WIDTH, TEXT_PREVIEW_HEIGHT)
