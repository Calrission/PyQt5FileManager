from database.EnterPointsRequests import EnterPointsRequests
from database.OpenTabsRequests import OpenTabsRequests


class DatabaseManager:
    def __init__(self):
        self.enter_points = EnterPointsRequests()
        self.open_tabs = OpenTabsRequests()
