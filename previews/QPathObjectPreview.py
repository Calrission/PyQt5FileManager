from common.PathObjects import PathObject
from widgets.QSmartWidget import QSmartWidget


class QPathObjectPreview(QSmartWidget):
    def __init__(self, x: int, y: int, path_object: PathObject, manager):
        super().__init__(x, y, manager)
        self.manager = manager
        self.path_object = path_object

    def _set_w_h_content(self):
        pass

    def initUI(self):
        self._set_w_h_content()


