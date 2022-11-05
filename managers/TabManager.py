from common.PathObjects import Folder
from common.Tab import Tab
from values.Exceptions import SelectTabErrorNotFound


class TabManager:
    def __init__(self, tabs_path=None,
                 on_add_tab=None,
                 on_remove_tab=None,
                 on_select_tab=None,
                 on_unselect_tab=None,
                 on_change_tab=None,
                 on_prepare=None):

        self.on_add_tab = on_add_tab
        self.on_remove_tab = on_remove_tab
        self.on_select_tab = on_select_tab
        self.on_unselect_tab = on_unselect_tab
        self.on_change_tab = on_change_tab
        self.on_prepare = on_prepare

        self._tabs = [Tab(i) for i in tabs_path] if tabs_path is not None else []

        self._select_tab_index = None

    def prepare(self):
        if len(self._tabs) != 0:
            self._select_tab_index = 0
            self.on_prepare(self._tabs, 0)

    def add_new_tab(self, path):
        tab = Tab(path)
        tab.add_on_change_folder(lambda folder: self.on_change_tab(self._get_tab_folder(folder)))
        self.add_tab(tab)

    def add_new_tabs(self, paths: list[str]):
        for path in paths:
            self.add_new_tab(path)

    def _get_tab_folder(self, folder: Folder):
        return [i for i in self._tabs if i.folder == folder][0]

    def add_tab(self, tab: Tab):
        self._tabs.append(tab)
        if self.on_add_tab is not None:
            self.on_add_tab(tab)
        if self._select_tab_index is None:
            self.select_tab(tab)

    def add_tabs(self, tabs: list[Tab]):
        for tab in tabs:
            self.add_tab(tab)

    def remove_tab(self, tab: Tab):
        if self._tabs.index(tab) == self._select_tab_index:
            self.select_tab(self.get(self._select_tab_index - 1))
        self._tabs.remove(tab)
        if self.on_remove_tab is not None:
            self.on_remove_tab(tab)

    def select_tab_index(self, index: int):
        tab = self._tabs[index]
        self.select_tab(tab)

    def select_tab(self, tab: Tab):
        if tab not in self._tabs:
            raise SelectTabErrorNotFound(tab)

        index = self._tabs.index(tab)

        if self._select_tab_index is not None:
            self.on_unselect_tab(self.get_select_tab())

        self._select_tab_index = index

        if self.on_select_tab is not None:
            self.on_select_tab(tab, index)

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
