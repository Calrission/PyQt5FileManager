from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import QtSvg


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

    @staticmethod
    def load_file_image_svg(file: str, w: int, h: int):
        svg = QtSvg.QSvgWidget(file)
        svg.setGeometry(0, 0, w, h)
        return svg
