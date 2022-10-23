from PyQt5.QtWidgets import QWidget

from Overlays import QOverlay


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
        return max(list(self._levels.keys()))

    def get_min_level(self):
        return min(list(self._levels.keys()))

    def remove_overlay(self, overlay: QOverlay):
        level_overlay = self.get_level_overlay(overlay)
        self._levels[level_overlay].remove(overlay)

    def remove_overlays(self, overlays: list[QOverlay]):
        for overlay in overlays:
            self.remove_overlay(overlay)

    def get_levels(self):
        return sorted(list(self._levels.keys()))

    def to_list(self):
        levels = self.get_levels()
        return [self._levels[i] for i in levels]


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

    def to_level_parent(self, overlay: QOverlay, level: int):
        sub_overlays = self._overlays[overlay]
        self._levels.move_all(sub_overlays, level)

    def to_top_level_parent(self, overlay: QOverlay):
        max_level = self._levels.get_max_level() + 1
        self.to_level_parent(overlay, max_level)

    def to_bottom_level_parent(self, overlay: QOverlay):
        min_level = self._levels.get_min_level() - 1
        self.to_level_parent(overlay, min_level)

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


class QWidgetOverlayManager(QWidget):
    def __init__(self):
        super().__init__()
        self.background_overlay = None
        self.manager = OverlayManager()

    def add_new_overlay(self, overlay: QOverlay, level=1):
        self.manager.add_parent_overlay(overlay, level)

    def show_overlay(self, overlay: QOverlay):
        overlay.show()

    def refresh(self):
        pass


