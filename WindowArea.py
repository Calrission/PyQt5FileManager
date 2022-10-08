from ConstValues import *
from PyQt5.QtWidgets import *
from enum import Enum
from PathObjects import *
from Tab import *


class Areas(Enum):
    TabPanel = (START_X_TP, END_X_TP, START_Y_TP, END_Y_TP, WIDTH_TP, HEIGHT_TP)
    MainPanel = (START_X_MP, END_X_MP, START_Y_MP, END_Y_MP, WIDTH_MP, HEIGHT_MP)
    LeftPanel = (START_X_LP, END_X_LP, START_Y_LP, END_Y_LP, WIDTH_LP, HEIGHT_LP)


class WindowArea:
    def __init__(self, window: QWidget,
                 start_x: int = None, end_x: int = None,
                 start_y: int = None, end_y: int = None,
                 width: int = None, height: int = None,
                 area: Areas = None):
        if area is None:
            self.end_y = end_y
            self.start_y = start_y
            self.end_x = end_x
            self.start_x = start_x
            self.width = width
            self.height = height
            self.window = window
        else:
            WindowArea.__init__(self, window=window,
                                start_x=area.value[0], end_x=area.value[1],
                                start_y=area.value[2], end_y=area.value[3],
                                width=area.value[4], height=area.value[5])

    def add_widget(self, widget: QWidget, x: int = None, y: int = None):
        x = widget.x() if x is None else x
        y = widget.y() if y is None else y

        widget.setParent(self.window)
        widget.move(x, y)
        widget.show()
        return widget


class TabWindowArea(WindowArea):
    def __init__(self, window: QWidget,
                 on_add_tab, on_select_tab,
                 on_remove_tab, on_unselect_tab,
                 start_x: int = None, end_x: int = None,
                 start_y: int = None, end_y: int = None,
                 width: int = None, height: int = None):
        super().__init__(window, start_x, end_x, start_y, end_y, width, height, Areas.TabPanel)

        self.on_remove_tab = on_remove_tab
        self.on_add_tab = on_add_tab
        self.on_select_tab = on_select_tab
        self.on_unselect_tab = on_unselect_tab

        self.tab_manager = TabManager(
            on_remove_tab=self._on_remove,
            on_add_tab=self._on_add,
            on_select_tab=self._on_select,
            on_unselect_tab=self._on_unselect,
            on_change_tab=self._on_change
        )
        self._tabs: list[QWidget] = []

    def generate_view_tab(self, tab: Tab):
        btn = self.add_widget(QPushButton(tab.name))
        new_x = self._calc_new_x()
        btn.move(new_x, self.start_y)
        btn.clicked.connect(self._click_tab)
        btn.show()
        return btn

    def _click_tab(self):
        view = self.window.sender()
        index = self._tabs.index(view)
        tab = self.tab_manager.get(index)
        self.tab_manager.select_tab(tab)

    def _on_add(self, tab: Tab):
        view = self.generate_view_tab(tab)
        self._tabs.append(view)
        self.on_add_tab(tab)

    def _calc_new_x(self):
        return sum([i.width() for i in self._tabs]) + 5 * (len(self._tabs) + 1)

    def _on_select(self, tab: Tab):
        view = self._tabs[self.tab_manager.index(tab)]
        if isinstance(view, QPushButton):
            view.setText("*" + view.text())
        self.on_select_tab(tab)

    def _on_unselect(self, tab: Tab):
        view = self._tabs[self.tab_manager.index(tab)]
        if isinstance(view, QPushButton):
            view.setText(view.text().replace("*", ""))
        self.on_unselect_tab(tab)

    def _on_remove(self, tab: Tab):
        view = self._tabs[self.tab_manager.index(tab)]
        view.deleteLater()
        self.on_remove_tab(tab)

    def _on_change(self, tab: Tab):
        view = self._tabs[self.tab_manager.index(tab)]
        if isinstance(view, QPushButton):
            view.setText(tab.name)
            if self.tab_manager.is_select_tab(tab):
                view.setText("*" + view.text())


class MainWindowArea(WindowArea):

    def __init__(self, window: QWidget,
                 start_x: int = None, end_x: int = None,
                 start_y: int = None, end_y: int = None,
                 width: int = None, height: int = None):
        super().__init__(window, start_x, end_x, start_y, end_y, width, height, Areas.MainPanel)

        self.widgets = [[]]
        self.max_column = self.width // (WIDTH_ITEM + MARGIN_ITEM)
        self.max_row = self.height // (HEIGHT_ITEM + MARGIN_ITEM)

        self._tab = None

    def _get_x_y_last_item(self):
        last_row = self.widgets[-1]
        y = (len(self.widgets) - 1) * (HEIGHT_ITEM + MARGIN_ITEM) + MARGIN_ITEM + self.start_y
        x = (len(last_row) - 1) * (WIDTH_ITEM + MARGIN_ITEM) + MARGIN_ITEM + self.start_x
        return x, y

    def _insert_new_widget(self, widget: QWidget):
        if len(self.widgets[-1]) >= self.max_column:
            self.widgets.append([])
        self.widgets[-1].append(widget)

    def add_item(self, widget: QWidget):
        self._insert_new_widget(widget)
        x, y = self._get_x_y_last_item()
        self.add_widget(widget, x, y)

    def add_items(self, data: list):
        [self.add_item(item) for item in data]

    def clear(self):
        [[j.deleteLater() for j in i] for i in self.widgets]
        self.widgets = [[]]

    def add_item_path_object(self, item: PathObject):
        btn = QPushButton(item.name)
        btn.resize(WIDTH_ITEM, HEIGHT_ITEM)
        if isinstance(item, Folder):
            btn.clicked.connect(self.click_folder)
        elif isinstance(item, File):
            btn.clicked.connect(item.open_default_app_os)
        self.add_item(btn)
        return btn

    def click_folder(self):
        btn = self.window.sender()
        folder_name = btn.text()
        self._tab.move_to_child_folder(folder_name)

    def set_new_content_tab(self):
        self.clear()
        [self.add_item_path_object(i) for i in self._tab.folder.children]

    def set_tab(self, tab: Tab):
        self._tab = tab
        self._tab.add_on_change_folder(lambda x: self.set_new_content_tab())
        self.set_new_content_tab()
