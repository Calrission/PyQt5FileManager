from OverlayManager import QWidgetOverlayManager
from Overlays import QActionPathObject, Action, QActionDeletePathObject, Result
from Tab import *
from QPathObjects import *
from QSwitchImageButton import *


class Areas(Enum):
    TabPanel = (START_X_TP, END_X_TP, START_Y_TP, END_Y_TP, WIDTH_TP, HEIGHT_TP, COLOR_BACKGROUND_TOP_RGB)
    MainPanel = (START_X_MP, END_X_MP, START_Y_MP, END_Y_MP, WIDTH_MP, HEIGHT_MP, COLOR_BACKGROUND_MAIN_RGB)
    LeftPanel = (START_X_LP, END_X_LP, START_Y_LP, END_Y_LP, WIDTH_LP, HEIGHT_LP, COLOR_BACKGROUND_LEFT_RGB)
    ButtonsPanel = (START_X_PANEL_BUTTONS, END_X_PANEL_BUTTONS, START_Y_PANEL_BUTTONS, END_Y_PANEL_BUTTONS,
                    WIDTH_PANEL_BUTTONS, HEIGHT_PANEL_BUTTONS, COLOR_BACKGROUND_TOP_RGB)
    App = (0, WIDTH - 1, 0, HEIGHT - 1, WIDTH, HEIGHT, COLOR_BACKGROUND_DEFAULT)


class WindowArea:
    def __init__(self, window: QWidgetOverlayManager,
                 start_x: int = None, end_x: int = None,
                 start_y: int = None, end_y: int = None,
                 width: int = None, height: int = None,
                 color_background: tuple = COLOR_BACKGROUND_DEFAULT,
                 area: Areas = None):
        if area is None:
            self.end_y = end_y
            self.start_y = start_y
            self.end_x = end_x
            self.start_x = start_x
            self.width = width
            self.height = height
            self.window = window
            self.color_background = color_background
        else:
            WindowArea.__init__(self, window=window,
                                start_x=area.value[0], end_x=area.value[1],
                                start_y=area.value[2], end_y=area.value[3],
                                width=area.value[4], height=area.value[5],
                                color_background=area.value[6])

        self.children: list[QWidget] = []

        self._delta_wheel_x = 0
        self._delta_wheel_y = 0

        self.background = QLabel()
        self.background.resize(self.width, self.height)
        self._add_widget(self.background, self.start_x, self.start_y)
        self.set_color_background_rgb(self.color_background)

    def add_widget(self, widget: QWidget, x: int = None, y: int = None):
        widget = self._add_widget(widget, x, y)
        self.children.append(widget)
        return widget

    def raise_(self):
        self.background.raise_()
        [i.raise_() for i in self.children]

    def _add_widget(self, widget: QWidget, x: int = None, y: int = None):
        x = widget.x() if x is None else x
        y = widget.y() if y is None else y
        widget.setMouseTracking(True)
        widget.setParent(self.window)
        widget.move(x, y)
        widget.show()
        return widget

    def get_bottom_widget(self):
        max_y = -1
        bottom_widget = None
        for widget in self.children:
            if widget.y() > max_y:
                bottom_widget = widget
                max_y = widget.y()
        return bottom_widget

    def get_top_widget(self):
        min_y = HEIGHT + 1
        top_widget = None
        for widget in self.children:
            if widget.y() < min_y:
                top_widget = widget
                min_y = widget.y()
        return top_widget

    def get_left_widget(self):
        min_x = WIDTH + 1
        left_widget = None
        for widget in self.children:
            if widget.x() < min_x:
                left_widget = widget
                min_x = widget.x()
        return left_widget

    def get_right_widget(self):
        max_x = -1
        right_widget = None
        for widget in self.children:
            if widget.x() > max_x:
                right_widget = widget
                max_x = widget.x()
        return right_widget

    def get_need_wheel_left(self):
        left_widget = self.get_left_widget()
        return left_widget.x() < self.start_x

    def get_need_wheel_right(self):
        right_widget = self.get_right_widget()
        return right_widget.x() + right_widget.width() > self.end_x

    def get_need_wheel_down(self):
        bottom_widget = self.get_bottom_widget()
        return bottom_widget.y() + bottom_widget.height() > HEIGHT

    def get_need_wheel_top(self):
        top_widget = self.get_top_widget()
        return top_widget.y() < self.start_y

    def delta_change_y_children(self, delta_y: int):
        self._delta_wheel_y += delta_y
        for widget in self.children:
            widget.move(widget.x(), widget.y() + delta_y)

    def delta_change_x_children(self, delta_x: int):
        self._delta_wheel_x += delta_x
        for widget in self.children:
            widget.move(widget.x() + delta_x, widget.y())

    def deleteLaterWidget(self, widget: QWidget):
        widget.deleteLater()
        if widget in self.children:
            self.children.remove(widget)

    def __str__(self):
        return self.__class__.__name__

    def set_color_background_rgb(self, color: tuple):
        UtilsVisual.set_background_color_label(self.background, color)


class TabWindowArea(WindowArea):
    def __init__(self, window: QWidgetOverlayManager,
                 on_add_tab, on_select_tab,
                 on_remove_tab, on_unselect_tab,
                 on_change_tab,):
        super().__init__(window, area=Areas.TabPanel)

        self.on_remove_tab = on_remove_tab
        self.on_add_tab = on_add_tab
        self.on_select_tab = on_select_tab
        self.on_unselect_tab = on_unselect_tab
        self.on_change_tab = on_change_tab

        self.tab_manager = TabManager(
            on_remove_tab=self._on_remove,
            on_add_tab=self._on_add,
            on_select_tab=self._on_select,
            on_unselect_tab=self._on_unselect,
            on_change_tab=self._on_change_folder
        )

    def generate_view_tab(self, tab: Tab):
        qtab = QTab(self.window, tab)
        new_x = self._calc_new_x()
        qtab.move(new_x, self.start_y + MARGIN_TAB_V_TP)
        qtab.mousePressEvent = lambda x: self._click_tab(qtab)
        qtab.show()
        return qtab

    def _click_tab(self, view):
        index = self.children.index(view)
        tab = self.tab_manager.get(index)
        self.tab_manager.select_tab(tab)

    def _on_add(self, tab: Tab):
        view = self.generate_view_tab(tab)
        self.children.append(view)
        self.on_add_tab(tab)

    def _calc_new_x(self):
        return self.start_x + sum([i.width() for i in self.children]) + MARGIN_TAB_H_TP * (len(self.children) + 1)

    def _on_select(self, tab: Tab):
        view = self.children[self.tab_manager.index(tab)]
        if isinstance(view, QTab):
            view.set_select(True)
        self.on_select_tab(tab)
        self._recalc_x_coord_children()

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


class MainWindowArea(WindowArea):

    def __init__(self, window: QWidgetOverlayManager):
        super().__init__(window, area=Areas.MainPanel)

        self.widgets = [[]]
        self.max_column = self.width // (WIDTH_ITEM + MARGIN_ITEM)
        self.max_row = self.height // (HEIGHT_ITEM + MARGIN_ITEM)

        self._tab = None

    def _get_x_y_new_last_item(self):
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
        x, y = self._get_x_y_new_last_item()
        self.add_widget(widget, x, y)

    def add_items(self, data: list):
        [self.add_item(item) for item in data]

    def clear(self):
        [[self.deleteLaterWidget(j) for j in i] for i in self.widgets]
        self.widgets = [[]]

    def create_view(self, obj: PathObject):
        if isinstance(obj, Folder):
            return QFolder(obj, self.window)
        elif isinstance(obj, File):
            return QFile(obj, self.window)
        else:
            return QPathObject(obj, self.window)

    def add_item_path_object(self, item: PathObject):
        view = self.create_view(item)
        view.mouseDoubleClickEvent = lambda event: self.get_func_action_click_path_object(item)(item)
        view.mousePressEvent = lambda event: self.click_mouse_item(event, item, view)
        self.add_item(view)
        return view

    def get_func_action_click_path_object(self, item: PathObject):
        if isinstance(item, Folder):
            return self.click_folder
        elif isinstance(item, File):
            return self.click_file

    def click_mouse_item(self, event, item: PathObject, view: QPathObject):
        if event.button() == Qt.RightButton:
            self.show_overlay_item(event.x() + view.x(), event.y() + view.y(), item)

    def show_overlay_item(self, x: int, y: int, item: PathObject):
        overlay = QActionPathObject.get_instance(item, x, y, self.window)
        overlay.clickItemEvent = self.eventItemOverlayPathObject
        self.window.add_new_overlay(overlay)
        self.window.show_overlay(overlay)

    def eventItemOverlayPathObject(self, action: Action, item: PathObject):
        self.window.dismiss_all()
        if action == Action.OPEN:
            self.get_func_action_click_path_object(item)(item)
        elif action == Action.DELETE:
            delete_overlay = QActionDeletePathObject(item, self.window)
            delete_overlay.ok = lambda obj: self.click_action_delete_ok(delete_overlay, obj)
            delete_overlay.cancel = lambda obj: self.click_action_delete_cancel(delete_overlay)
            self.window.add_new_overlay(delete_overlay)
            self.window.show_overlay(delete_overlay)

    def click_action_delete_ok(self, overlay: QActionDeletePathObject, obj: PathObject):
        self.window.dismiss_parent(overlay)
        self.remove_path_object(obj)

    def remove_path_object(self, path_object: PathObject):
        path_object.delete()
        widget = self.get_widget_path_object(path_object)
        self.children.remove(widget)
        widget.deleteLater()

    def get_widget_path_object(self, path_object: PathObject):
        for widget in [j for i in self.widgets for j in i]:
            if widget.obj == path_object:
                return widget
        raise ValueError(f"Widget for {path_object} in MainAreaWindow not found")

    def click_action_delete_cancel(self, overlay: QActionDeletePathObject):
        self.window.dismiss_parent(overlay)

    def click_folder(self, item: Folder):
        r, c = self.index_path_object(item)
        index = r * self.max_column + c
        obj = self._tab.folder.children[index]
        if not isinstance(obj, Folder):
            raise ValueError("Click folder to not folder object in MainAreaWindow")
        folder_name = obj.name
        self._tab.move_to_child_folder(folder_name)

    def click_file(self, item: File):
        item.open_default_app_os()

    def index_path_object(self, path_object: PathObject):
        for i_r, r in enumerate(self.widgets):
            for i_c, c in enumerate(r):
                if c.obj == path_object:
                    return i_r, i_c
        raise ValueError(f"{path_object} not found in MainAreaWindow")

    def index(self, widget: QWidget):
        for i_r, r in enumerate(self.widgets):
            for i_c, c in enumerate(r):
                if c == widget:
                    return i_r, i_c
        raise ValueError(f"{widget} not found in MainAreaWindow")

    def set_new_content_tab(self):
        self.clear()
        [self.add_item_path_object(i) for i in self._tab.folder.children]

    def set_tab(self, tab: Tab):
        self._tab = tab
        self._tab.add_on_change_folder(lambda x: self.set_new_content_tab())
        self.set_new_content_tab()

    def get_tab(self):
        return self._tab


class ButtonsAreaWindow(WindowArea):
    def __init__(self, window: QWidgetOverlayManager, click_back_history, click_next_history, click_setting):
        super().__init__(window, area=Areas.ButtonsPanel)

        self.click_next_history = click_next_history
        self.click_back_history = click_back_history
        self.click_setting = click_setting

        self.next_h = QSwitchImageButton(self.window, TypeImageButton.RIGHT)
        self.next_h.move(START_X_HISTORY_BUTTON + WIDTH_BUTTON + MARGIN_BUTTON_HISTORY, START_Y_BUTTON)
        self.prev_h = QSwitchImageButton(self.window, TypeImageButton.LEFT)
        self.prev_h.move(START_X_HISTORY_BUTTON, START_Y_BUTTON)
        self.prev_h.set_click(self.click_back_history)
        self.next_h.set_click(self.click_next_history)

        self.setting = QSwitchImageButton(self.window, TypeImageButton.SETTINGS)
        self.setting.move(START_X_SETTING, START_Y_BUTTON)
        self.setting.set_click(self.click_setting)
        self.setting.setEnabled(True)

        self.children = [self.prev_h, self.next_h, self.setting]
