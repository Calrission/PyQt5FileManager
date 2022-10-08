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
    def __init__(self, now_path: str = "", func_for_select=None):
        self.folder = Folder(now_path)
        self.folder.refresh()
        self.name = self.folder.get_short_name()
        self.selector = FileSelector(self.folder.children)
        self.on_select_file = func_for_select
        self._on_change_folder = []
        self.history = HistoryTab([now_path])

    def move_to_child_folder(self, folder_name: str):
        self.folder.next(folder_name)
        self._refresh_on_change_folder()

    def move_to_folder(self, folder_path: str):
        self.folder.change(folder_path)
        self._refresh_on_change_folder()

    def add_on_change_folder(self, func):
        self._on_change_folder.append(func)

    def _call_on_change_folder(self):
        [i(self.folder) for i in self._on_change_folder]

    def _refresh_on_change_folder(self):
        self.folder.refresh()
        self.name = self.folder.get_short_name()
        self.selector.change_origin_files(self.folder.children)
        self.history.add(self.folder.path)
        if self._on_change_folder is not None:
            self._call_on_change_folder()

    def move_back_history(self):
        self.history.next_path = self.folder.path
        self.folder = Folder(self.history.to_prev())
        self.selector.change_origin_files(self.folder.children)

    def move_next_history(self):
        if self.history.next_path is not None:
            self.move_to_folder(self.history.pop_next_path())

    def open_file(self, file_name: str):
        self.folder.get_file(file_name).open_default_app_os()

    def __str__(self):
        return self.folder.path


class TabManager:
    def __init__(self, tabs=None,
                 on_add_tab=None,
                 on_remove_tab=None,
                 on_select_tab=None,
                 on_unselect_tab=None,
                 on_change_tab=None):

        self.on_add_tab = on_add_tab
        self.on_remove_tab = on_remove_tab
        self.on_select_tab = on_select_tab
        self.on_unselect_tab = on_unselect_tab
        self.on_change_tab = on_change_tab

        self._select_tab_index = None

        self._tabs = tabs if tabs is not None else []

    def add_new_tab(self, path=""):
        tab = Tab(path)
        tab.add_on_change_folder(lambda folder: self.on_change_tab(self._get_tab_folder(folder)))
        self.add_tab(tab)

    def _get_tab_folder(self, folder: Folder):
        return [i for i in self._tabs if i.folder == folder][0]

    def add_tab(self, tab: Tab):
        self._tabs.append(tab)
        if self.on_add_tab is not None:
            self.on_add_tab(tab)
        if self._select_tab_index is None:
            self.select_tab(tab)

    def remove_tab(self, tab: Tab):
        if self._tabs.index(tab) == self._select_tab_index:
            self.select_tab(self.get(self._select_tab_index - 1))
        self._tabs.remove(tab)
        if self.on_remove_tab is not None:
            self.on_remove_tab(tab)

    def select_tab(self, tab: Tab):
        if tab not in self._tabs:
            raise SelectTabErrorNotFound(tab)

        if self._select_tab_index is not None:
            self.on_unselect_tab(self.get_select_tab())

        self._select_tab_index = self._tabs.index(tab)

        if self.on_select_tab is not None:
            self.on_select_tab(tab)

    def is_select_tab(self, tab: Tab):
        return self.get_select_tab() == tab

    def get(self, index: int):
        return self._tabs[index]

    def get_select_tab(self):
        return self._tabs[self._select_tab_index]

    def get_all_tabs(self):
        return self._tabs

    def index(self, tab: Tab):
        return self._tabs.index(tab)