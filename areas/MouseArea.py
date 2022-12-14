from areas.WindowArea import WindowArea


class MouseArea:
    def __init__(self, areas: list[WindowArea]):
        self.areas = areas
        self.last_x_y = (0, 0)

    def mouseMoveEvent(self, event):
        self.last_x_y = (event.x(), event.y())

    def get_area_last_detect_mouse(self) -> WindowArea:
        for area in self.areas:
            if (area.start_x <= self.last_x_y[0] <= area.end_x) and (area.start_y <= self.last_x_y[1] <= area.end_y):
                return area
        raise ValueError("get area last detect mouse not found")
