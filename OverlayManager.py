from enum import Enum
from PyQt5.QtWidgets import QWidget, QLabel
from ConstValues import WIDTH, HEIGHT
from Overlays import QOverlay, QActionAlertDialog
from UtilsVisual import UtilsVisual


class LevelsOverlays:
    def __init__(self, levels: dict[int: list[QOverlay]]):
        self._levels = levels

    def get_level_overlay(self, overlay: QOverlay):
        for level in self._levels:
            overlays_level = self._levels[level]
            if overlay in overlays_level:
                return level
        raise ValueError(f"{repr(overlay)} not found")

    def get_overlays(self, level: int):
        return self._levels[level]

    def add_overlay(self, overlay: QOverlay, level: int):
        if level in self._levels:
            self._levels[level].append(overlay)
        else:
            self._levels[level] = [overlay]

    def add_sub_overlay(self, parent_overlay: QOverlay, sub_overlay: QOverlay):
        parent_level = self.get_level_overlay(parent_overlay)
        self.add_overlay(sub_overlay, parent_level)

    def move(self, overlay: QOverlay, new_level: int):
        now_level = self.get_level_overlay(overlay)
        self._levels[now_level].remove(overlay)
        self.add_overlay(overlay, new_level)

    def move_all(self, overlays: list[QOverlay], new_level: int):
        for overlay in overlays:
            self.move(overlay, new_level)

    def get_max_level(self):
        if len(self._levels.keys()) == 0:
            return 0
        return max(list(self._levels.keys()))

    def get_min_level(self):
        if len(self._levels.keys()) == 0:
            return 0
        return min(list(self._levels.keys()))

    def remove_overlay(self, overlay: QOverlay):
        level_overlay = self.get_level_overlay(overlay)
        self._levels[level_overlay].remove(overlay)

    def remove_overlays(self, overlays: list[QOverlay]):
        for overlay in overlays:
            self.remove_overlay(overlay)
        self._clear_empty_levels()

    def _clear_empty_levels(self):
        empty_levels = [i for i in list(self._levels.keys()) if len(self._levels[i]) == 0]
        for level in empty_levels:
            del self._levels[level]

    def get_levels(self):
        return sorted(list(self._levels.keys()))

    def to_list(self):
        levels = self.get_levels()
        return [self._levels[i] for i in levels]

    def clear(self):
        self._levels = {}


class OverlayManager:
    def __init__(self, overlays_parent: list[QOverlay] = None):
        if overlays_parent is None:
            overlays_parent = []
        self._overlays = {i: [] for i in overlays_parent}
        self._levels = LevelsOverlays({
            1: overlays_parent
        })

    def add_parent_overlay(self, overlay: QOverlay, level: int = 1):
        self._overlays[overlay] = []
        self._levels.add_overlay(overlay, level)

    def add_sub_overlay(self, parent_overlay: QOverlay, sub_overlay: QOverlay):
        self._overlays[parent_overlay].append(sub_overlay)
        self._levels.add_sub_overlay(parent_overlay, sub_overlay)

    def get_parents_level(self, level: int):
        overlays_level = self._levels.get_overlays(level)
        return list(filter(lambda x: x in self._overlays, overlays_level))

    def get_parents(self):
        return list(self._overlays.keys())

    def get_sub_overlays_parent(self, overlay: QOverlay):
        return self._overlays[overlay]

    def get_parent_from_sub_overlay(self, overlay: QOverlay):
        for parent_overlay in self._overlays:
            sub_overlays = self._overlays[parent_overlay]
            if overlay in sub_overlays:
                return parent_overlay
        raise ValueError(f"parent for {repr(overlay)} not found")

    def remove_parent_overlay(self, overlay: QOverlay):
        sub_overlays = self._overlays[overlay]
        self._levels.remove_overlays([overlay] + sub_overlays)
        del self._overlays[overlay]

    def remove_sub_overlay(self, sub_overlay: QOverlay):
        parent_overlay = self.get_parent_from_sub_overlay(sub_overlay)
        self._levels.remove_overlay(sub_overlay)
        self._overlays[parent_overlay].remove(sub_overlay)

    def remove_all(self):
        self._levels.clear()
        self._overlays = {}

    def to_level_parent(self, overlay: QOverlay, level: int):
        sub_overlays = self._overlays[overlay]
        self._levels.move_all(sub_overlays, level)

    def to_top_level_parent(self, overlay: QOverlay):
        max_level = self._levels.get_max_level() + 1
        self.to_level_parent(overlay, max_level)

    def to_bottom_level_parent(self, overlay: QOverlay):
        min_level = self._levels.get_min_level() - 1
        self.to_level_parent(overlay, min_level)

    def max(self):
        return self._levels.get_max_level()

    def min(self):
        return self._levels.get_min_level()

    def is_parent(self, overlay: QOverlay):
        return overlay in self._overlays

    def is_sub(self, overlay: QOverlay):
        return not self.is_parent(overlay)

    def to_list(self):
        lst = []
        for level in self._levels.get_levels():
            level_overlays = []
            parents_level = self.get_parents_level(level)
            for parent in parents_level:
                sub_overlays = self.get_sub_overlays_parent(parent)
                level_overlays.append([parent] + sub_overlays)
            lst.append(level_overlays)
        return lst


class ModeOverlayManager(Enum):
    MULTY = 0
    SINGLE = 1


class QWidgetOverlayManager(QWidget):
    def __init__(self, mode: ModeOverlayManager = ModeOverlayManager.SINGLE):
        super().__init__()
        self.mode = mode
        self.background_overlay = QLabel(self)
        self.background_overlay.resize(WIDTH, HEIGHT)
        self.background_overlay.mousePressEvent = lambda x: self._click_background()
        UtilsVisual.set_background_color_label(self.background_overlay, (0, 0, 0), WIDTH, HEIGHT, 190)
        self.manager = OverlayManager()
        self.active_overlays = []

    def dismiss_all(self):
        for parent in self.manager.get_parents():
            overlays = self.manager.get_sub_overlays_parent(parent)
            self.manager.remove_parent_overlay(parent)
            self.active_overlays = []
            for i in [parent] + overlays:
                i.hide()
                i.deleteLater()
        self.manager.remove_all()
        self.background_overlay.hide()

    def dismiss_parent(self, parent):
        overlays = self.manager.get_sub_overlays_parent(parent)
        self.manager.remove_parent_overlay(parent)
        if parent in self.active_overlays:
            self.active_overlays.remove(parent)
        for i in [parent] + overlays:
            i.hide()
            i.deleteLater()
        if len(self.active_overlays) == 0:
            self.background_overlay.hide()
            self.background_overlay.lower()

    def dismiss_sub(self, parent):
        pass

    def add_new_overlay(self, overlay: QOverlay, level=1):
        if self.mode == ModeOverlayManager.SINGLE:
            self.dismiss_all()
        self.manager.add_parent_overlay(overlay, level)
        self.refresh()

    def add_sub_overlay(self, overlay: QOverlay, parent: QOverlay):
        self.manager.add_sub_overlay(overlay, parent)
        self.refresh()

    def _click_background(self):
        for overlay in self.active_overlays:
            self.dismiss_all()
        self.background_overlay.hide()

    def refresh(self):
        for level in self.manager.to_list():
            for group in level:
                for overlay in group:
                    if isinstance(overlay, QOverlay):
                        overlay.raise_()

    def show_overlay(self, overlay: QOverlay):
        self._show_background()
        self.active_overlays.append(overlay)
        overlay.show()

    def _show_background(self):
        self.background_overlay.raise_()
        self.background_overlay.show()

    def show_error(self, message):
        error_overlay = QActionAlertDialog(message, self)
        error_overlay.set_positive("OK", lambda: self.dismiss_parent(error_overlay))
        self.add_new_overlay(error_overlay, self.manager.max() + 1)
        self.show_overlay(error_overlay)

    def is_active(self):
        return len(self.active_overlays) != 0
