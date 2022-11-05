from PyQt5.QtWidgets import QWidget
from common.Tab import Tab
from areas.WindowArea import WindowArea
from managers.OverlayManager import QWidgetOverlayManager
from managers.TabManager import TabManager
from values.Areas import Areas
from values.ConstValues import MARGIN_TAB_V_TP, MARGIN_TAB_H_TP
from widgets.QTab import QTab


class TabWindowArea(WindowArea):
    def __init__(self, window: QWidgetOverlayManager,
                 on_add_tab, on_select_tab,
                 on_remove_tab, on_unselect_tab,
                 on_prepare, on_change_tab,
                 tabs):
        super().__init__(window, area=Areas.TabPanel)

        self.on_remove_tab = on_remove_tab
        self.on_add_tab = on_add_tab
        self.on_select_tab = on_select_tab
        self.on_unselect_tab = on_unselect_tab
        self.on_change_tab = on_change_tab
        self.on_prepare = on_prepare

        self.tab_manager = TabManager(
            on_remove_tab=self._on_remove,
            on_add_tab=self._on_add,
            on_select_tab=self._on_select,
            on_unselect_tab=self._on_unselect,
            on_change_tab=self._on_change_folder,
            on_prepare=self._on_prepare,
            tabs_path=tabs
        )

    def prepare(self):
        self.tab_manager.prepare()

    def generate_view_tab(self, tab: Tab):
        qtab = QTab(self.window, tab)
        new_x = self._calc_new_x()
        qtab.move(new_x, self.start_y + MARGIN_TAB_V_TP)
        qtab.mousePressEvent = lambda x: self._click_tab(qtab)
        qtab.show()
        return qtab

    def _on_prepare(self, tabs: list, select_index: int):
        for tab in tabs:
            self._generate_new_view_tab(tab)
        self._on_select(tabs[select_index], select_index)
        if self.on_prepare is not None:
            self.on_prepare(tabs, select_index)

    def _generate_new_view_tab(self, tab: Tab):
        view = self.generate_view_tab(tab)
        self.children.append(view)

    def _click_tab(self, view):
        index = self.children.index(view)
        tab = self.tab_manager.get(index)
        self.tab_manager.select_tab(tab)

    def _on_add(self, tab: Tab):
        self._generate_new_view_tab(tab)
        self.on_add_tab(tab)

    def _calc_new_x(self):
        return self.start_x + sum([i.width() for i in self.children]) + MARGIN_TAB_H_TP * (len(self.children) + 1)

    def _select_view_tab(self, index: int):
        view = self.children[index]
        if isinstance(view, QTab):
            view.set_select(True)
        self._recalc_x_coord_children()

    def _on_select(self, tab: Tab, index: int):
        self._select_view_tab(index)
        self.on_select_tab(tab, index)

    def _on_unselect(self, tab: Tab):
        view = self.children[self.tab_manager.index(tab)]
        if isinstance(view, QTab):
            view.set_select(False)
        self.on_unselect_tab(tab)

    def _on_remove(self, tab: Tab):
        view = self.children[self.tab_manager.index(tab)]
        self.deleteLaterWidget(view)
        self.on_remove_tab(tab)

    def _recalc_x_coord_children(self):
        item_x = self.start_x + MARGIN_TAB_H_TP + self._delta_wheel_x
        for item in self.children:
            if isinstance(item, QWidget):
                item.move(item_x, item.y())
                item_x += item.width() + MARGIN_TAB_H_TP

    def _on_change_folder(self, tab: Tab):
        view = self.children[self.tab_manager.index(tab)]
        if isinstance(view, QTab):
            view.setText(tab.name)
        self.on_change_tab(tab)
        self._recalc_x_coord_children()
