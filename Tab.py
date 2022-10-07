from HistoryTab import HistoryTab
from PathObjects import *


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


class Tab:
    def __init__(self, now_path: str, func_for_select=None):
        self.folder = Folder(now_path)
        self.selector = FileSelector(self.folder.children)
        self.func_for_select = func_for_select
        self.history = HistoryTab([now_path])

    def move_to_child_folder(self, folder_name: str):
        self.folder.next(folder_name)
        self.refresh_on_change_folder()

    def move_to_folder(self, folder_path: str):
        self.folder.change(folder_path)
        self.refresh_on_change_folder()

    def refresh_on_change_folder(self):
        self.selector.change_origin_files(self.folder.children)
        self.history.add(self.folder.path)

    def move_back_history(self):
        self.history.next_path = self.folder.path
        self.folder = Folder(self.history.to_prev())
        self.selector.change_origin_files(self.folder.children)

    def move_next_history(self):
        if self.history.next_path is not None:
            self.move_to_folder(self.history.pop_next_path())

    def open_file(self, file_name: str):
        self.folder.get_file(file_name).open_default_app_os()
