from PyQt5.QtWidgets import QWidget
from common.PathObjects import PathObject, TypePathObject
from overlays.QActionAlertDialog import QActionAlertDialog


class QActionDeletePathObject(QActionAlertDialog):
    def __init__(self, path_object: PathObject, parent: QWidget, click_ok, click_cancel):
        self.path_object = path_object
        message = self._calc_message()
        super().__init__(message, parent)
        self._negative_txt = "Cancel"
        self._positive_txt = "OK"
        self._positive = click_ok
        self._negative = click_cancel

    def _calc_message(self) -> str:
        object_ = 'папку' if self.path_object.type == TypePathObject.FOLDER else \
            'файл' if self.path_object.type == TypePathObject.FILE else ''
        return f"Вы действительно хотите удалить {object_} \"{self.path_object.name}\"?"

    def _click_positive(self):
        self._positive(self.path_object)

    def _click_negative(self):
        self._negative(self.path_object)