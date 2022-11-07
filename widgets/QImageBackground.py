from PyQt5.QtWidgets import QWidget

from widgets.QImageView import QImageView


class QImageBackground(QWidget):
    def __init__(self, parent: QWidget, image: str):
        super().__init__(parent)
        self.image = image
        self.image_widget = None

    def init_background(self, w: int, h: int):
        if self.image_widget is not None:
            self.image_widget.deleteLater()
        self.image_widget = QImageView(self, path=self.image)
        self.image_widget.mousePressEvent = lambda x: None
        self.image_widget.resize(w, h)
        self.image_widget.lower()


