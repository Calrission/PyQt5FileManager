from common.PathObjects import PathObject
from widgets.QSmartWidget import QSmartWidget


class QPathObjectPreview(QSmartWidget):
    def __init__(self, x: int, y: int, path_object: PathObject, parent):
        super().__init__(x, y, parent)
        self.path_object = path_object

    def initUI(self):
        pass