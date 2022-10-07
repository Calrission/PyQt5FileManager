class HistoryTab:
    def __init__(self, history=None):
        self.next_path = None
        self.__history = history if history is not None else []

    def now(self):
        return self.__history[-1]

    def add(self, path: str):
        self.__history.append(path)

    def pop_next_path(self):
        path = self.next_path
        self.next_path = None
        return path

    def get(self):
        return self.__history

    def to_prev(self):
        self.add(self.__history[-2])
        return self.now()
