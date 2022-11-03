class FileSelector:
    def __init__(self, origin_files: list):
        self.__origin_files = [i for i in origin_files]
        self.last_single_select = None
        self.selected = []

    def change_origin_files(self, files: list):
        self.__init__(files)

    def single_select(self, file_name: str):
        self.last_single_select = self.__origin_files.index(file_name)
        self.selected.append(file_name)

    def single_unselect(self, file_name: str):
        self.selected.remove(file_name)
        self.last_single_select = None

    def multi_unselect(self):
        self.selected = []
        self.last_single_select = None

    def multi_select(self, file_name):
        start_select = self.__origin_files.index(self.last_single_select)
        end_select = self.__origin_files.index(file_name)
        if end_select < start_select:
            start_select, end_select = end_select, start_select
        self.selected = self.__origin_files[start_select: end_select + 1]