from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QColor


class ImageLoaderPixmap:
    @staticmethod
    def load_file_to_label(file_path: str, label: QLabel):
        pixmap = QPixmap(file_path)
        label.setPixmap(pixmap)

    @staticmethod
    def set_background_color_label(label: QLabel, color: tuple):
        pixmap = QPixmap(label.width(), label.height())
        pixmap.fill(QColor(*color))
        label.setPixmap(pixmap)
