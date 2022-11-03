from values.ConstValues import HEIGHT_BUTTON, WIDTH_BUTTON
from values.TypeImageButton import TypeImageButton
from widgets.QImageView import QImageView


class QSwitchImageButton(QImageView):
    def __init__(self, parent, type_: TypeImageButton):
        super().__init__(parent=parent)

        self.resize(WIDTH_BUTTON, HEIGHT_BUTTON)

        self.states = type_.value
        self.mousePressEvent = lambda x: (self.click() if self.click is not None else None)
        self.setEnabled(False)

    def setEnabled(self, bool_: bool):
        super().setEnabled(bool_)
        self._setImage(self.states[int(bool_)])

    def setImage(self, path: str):
        try:
            index = self.states.index(path)
        except IndexError:
            index = 0
        self.setEnabled(bool(index))
