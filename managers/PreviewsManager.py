from previews.QPathObjectPreview import QPathObjectPreview
from widgets.QAlphaDarkBackground import QAlphaDarkBackground


class PreviewsManager(QAlphaDarkBackground):
    def __init__(self):
        super().__init__()
        self.active_preview = None

    def show_preview(self, preview: QPathObjectPreview):
        if self.active_preview is not None:
            self.dismiss_active_preview()

        self.active_preview = preview
        self.show_background()
        preview.show()

    def dismiss_active_preview(self):
        if self.active_preview is not None:
            self.active_preview.deleteLater()
            self.active_preview = None

    def press_background(self, *args):
        super().press_background(*args)
        self.dismiss_active_preview()

    def is_active(self):
        return self.active_preview is not None

