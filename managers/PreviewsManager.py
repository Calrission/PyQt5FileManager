from previews.QPathObjectPreview import QPathObjectPreview


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