from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QColor
from PyQt5 import QtSvg


class UtilsVisual:
    @staticmethod
    def load_file_to_label(file_path: str, label: QLabel):
        pixmap = QPixmap(file_path)
        label.setPixmap(pixmap)

    @staticmethod
    def set_background_color_label(label: QLabel, color: tuple, w: int = None, h: int = None, alpha: int = 255):
        w = w if w is not None else label.width()
        h = h if h is not None else label.height()
        pixmap = QPixmap(w, h)
        pixmap.fill(QColor(*color, alpha=alpha))
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

    @staticmethod
    def get_w_h_image(file_path: str):
        pixmap = QPixmap(file_path)
        return pixmap.size().width(), pixmap.size().height()
