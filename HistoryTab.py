class HistoryTab:
    def __init__(self, history=None):
        self.__history = history if history is not None else []

    def now(self):
        return self.__history[-1]

    def add(self, path: str):
        self.__history.append(path)

    def get(self):
        return self.__history

    def get_prev(self):
        return self.__history[-2]

    def can_prev(self):
        return len(self.__history) >= 2
