from PyQt5.QtWidgets import QWidget
from common.PathObjects import PathObject
from overlays.QActionLineEdit import QActionLineEdit


class QActionRenamePathObject(QActionLineEdit):
    def __init__(self, parent: QWidget, path_object: PathObject, positive, negative):
        super().__init__(parent, "Переименовать", path_object.name)
        self.path_object = path_object
        self._positive_txt = "OK"
        self._positive = positive
        self._negative = negative
        self._negative_txt = "Отмена"

    def _click_positive(self):
        self._positive(self.new_name.text(), self.path_object)

    def _click_negative(self):
        self._negative(self.path_object)