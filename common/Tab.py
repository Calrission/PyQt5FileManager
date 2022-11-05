from common.PathObjects import *
from common.FileSelector import FileSelector
from common.HistoryTab import HistoryTab


class Tab:
    def __init__(self, now_path: str = "", func_for_select=None):
        self.folder = Folder(now_path)
        self.folder.refresh()
        self.next_path = []
        self.name = self.folder.get_short_name()
        self.selector = FileSelector(self.folder.children)
        self.on_select_file = func_for_select
        self._on_change_folder = []
        self.history = HistoryTab([self.folder.path])

    def move_to_child_folder(self, folder_name: str):
        last_folder = self.folder.path
        self.folder.next(folder_name)
        self._refresh_on_change_folder(last_folder)

    def move_to_folder(self, folder_path: str):
        last_folder = self.folder.path
        self.folder.change(folder_path)
        self._refresh_on_change_folder(last_folder)

    def add_on_change_folder(self, func):
        self._on_change_folder.append(func)

    def _call_on_change_folder(self, last_folder: str):
        [i(last_folder, self.folder) for i in self._on_change_folder]

    def _refresh_on_change_folder(self, last_folder: str):
        self.folder.refresh()
        self.name = self.folder.get_short_name()
        self.selector.change_origin_files(self.folder.children)
        self.history.add(self.folder.path)
        if self._on_change_folder is not None:
            self._call_on_change_folder(last_folder)

    def move_back_parent(self):
        self.move_to_folder(self.folder.get_parent_folder_path())
        self.selector.change_origin_files(self.folder.children)

    def move_next_history(self):
        if self.history.can_next():
            self.move_to_folder(self.history.get_next())

    def move_prev_history(self):
        if self.history.can_prev():
            self.move_to_folder(self.history.get_prev())

    def open_file(self, file_name: str):
        self.folder.get_file(file_name).open_default_app_os()

    def __str__(self):
        return self.folder.path
