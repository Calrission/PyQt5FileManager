from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QColor


class UtilsVisual:
    @staticmethod
    def load_file_to_label(file_path: str, label: QLabel):
        pixmap = QPixmap(file_path)
        label.setPixmap(pixmap)

    @staticmethod
    def set_background_color_label(label: QLabel, color: tuple):
        pixmap = QPixmap(label.width(), label.height())
        pixmap.fill(QColor(*color))
        label.setPixmap(pixmap)

    @staticmethod
    def load_file_to_label_with_scaled(file_path: str, label: QLabel, scaled: tuple):
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(*scaled)
        label.setPixmap(pixmap)
