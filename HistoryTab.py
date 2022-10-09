class HistoryTab:
    def __init__(self, history=None):
        self.__history = history if history is not None else []
        self.__history_back = []
        self.__history_next = []

    def now(self):
        return self.__history[-1]

    def add(self, path: str):
        if len(self.__history_next) != 0 and path == self.__history_next[-1]:
            self.__history_next = self.__history_next[:-1]
            self.__history_back.append(self.now())
        elif len(self.__history_back) != 0 and path == self.__history_back[-1]:
            self.__history_back = self.__history_back[:-1]
            self.__history_next.append(self.now())
        else:
            self.__history_back.append(self.now())
            self.__history_next.clear()
        self.__history.append(path)

    def get(self, index):
        return self.__history[index]

    def get_prev(self):
        return self.__history_back[-1]

    def get_next(self):
        return self.__history_next[-1]

    def can_prev(self):
        return len(self.__history_back) != 0

    def can_next(self):
        return len(self.__history_next) != 0
