from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel
from common.Tab import Tab
from common.UtilsVisual import UtilsVisual
from values.ConstValues import HEIGHT_TAB_TP, COLOR_TEXT, PADDING_TAB


class QTab(QWidget):
    def __init__(self, parent, tab: Tab):
        super().__init__(parent=parent)
        self.tab = tab

        self.backgrounds = ["files/back_tab.png", "files/back_tag_select.png"]

        self.is_select = False

        self._image = QLabel(self)
        self._text_view = QLabel(self)

        self._setupText()

        self.resize(self.width(), HEIGHT_TAB_TP)

        self.setText(tab.name)

        self._reset_pixmap_background_tab()

    def set_select(self, is_select):
        self.is_select = is_select
        self._reset_pixmap_background_tab()

    def _setupText(self):
        values = ", ".join([str(i) for i in COLOR_TEXT])
        self._text_view.setStyleSheet("QLabel { color: rgb(" + values + "); }")

    def _reset_pixmap_background_tab(self):
        UtilsVisual.load_file_to_label_with_scaled(self.backgrounds[int(self.is_select)], self._image,
                                                   (self.width(), self.height()))
        self._image.resize(self.width(), self.height())

    def setText(self, text: str):
        self._text_view.setText(text)
        self._text_view.show()
        self._text_view.adjustSize()
        self._text_view.setAlignment(Qt.AlignVCenter)
        self.resize(self._text_view.width() + 2 * PADDING_TAB, self.height())
        self._text_view.move(PADDING_TAB, int(self.height() / 2 - self._text_view.height() / 2))
        self._reset_pixmap_background_tab()

    def text(self):
        return self._text_view.text()
