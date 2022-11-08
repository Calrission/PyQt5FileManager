from overlays.QActionMenu import QActionMenu
from values.Action import Action


class QActionFavorite(QActionMenu):
    def __init__(self, x: int, y: int, parent, favorite_path: str):
        super().__init__(x, y, parent, [Action.REMOVE_FAVORITE])
        self.favorite_path = favorite_path

    def _click_item_event(self, action: Action):
        self.clickItemEvent(action, self.favorite_path)