from common.PathObjects import Folder
from widgets.QPathObject import QPathObject


class QFolder(QPathObject):
    def __init__(self, folder: Folder, parent=None):
        QPathObject.__init__(self, folder, parent=parent, icon="files/folder.png")