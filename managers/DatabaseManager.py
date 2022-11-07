from database.EnterPointsRequests import EnterPointsRequests
from database.InitorRequests import InitorRequests
from database.OpenTabsRequests import OpenTabsRequests


class DatabaseManager:
    def __init__(self):
        self.initor = InitorRequests()
        self.enter_points = EnterPointsRequests()
        self.open_tabs = OpenTabsRequests()
        self.initor.init_all_tables()