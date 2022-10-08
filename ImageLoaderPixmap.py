from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap


class ImageLoaderPixmap:
    @staticmethod
    def loadToLabel(file_path: str, label: QLabel):
        pixmap = QPixmap(file_path)
        label.setPixmap(pixmap)


