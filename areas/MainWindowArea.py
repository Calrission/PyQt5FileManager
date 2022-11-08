from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget
from common.PathObjects import PathObject, Folder, File, TypePathObject
from common.PreviewsFactory import PreviewsFactory
from common.Tab import Tab
from areas.WindowArea import WindowArea
from managers.DatabaseManager import DatabaseManager
from managers.OverlayManager import QWidgetOverlayManager
from managers.PreviewsManager import PreviewsManager
from overlays.QActionAlertDialog import QActionAlertDialog
from overlays.QActionDeletePathObject import QActionDeletePathObject
from overlays.QActionLineEdit import QActionLineEdit
from overlays.QActionMenu import QActionMenu
from overlays.QActionPathObject import QActionPathObject
from overlays.QActionRenamePathObject import QActionRenamePathObject
from overlays.QOverlay import QOverlay
from values.Action import Action
from values.Areas import Areas
from values.ConstValues import WIDTH_ITEM, MARGIN_ITEM, HEIGHT_ITEM
from widgets.QFile import QFile
from widgets.QFolder import QFolder
from widgets.QPathObject import QPathObject


class MainWindowArea(WindowArea):

    def __init__(self, window: QWidgetOverlayManager,
                 preview_manager: PreviewsManager,
                 db_manager: DatabaseManager,
                 on_favorite=None,
                 on_new_tab=None):
        super().__init__(window, area=Areas.MainPanel)

        self.widgets = [[]]
        self.db_manager = db_manager
        self.preview_manager = preview_manager
        self.max_column = self.width // (WIDTH_ITEM + MARGIN_ITEM)
        self.max_row = self.height // (HEIGHT_ITEM + MARGIN_ITEM)

        self._tab = None
        self.on_new_tab = on_new_tab
        self.on_change_favorite = on_favorite

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
        overlay = QActionPathObject.get_instance(item, x, y, self.window, self.db_manager)
        overlay.clickItemEvent = self.eventItemOverlayPathObject
        self.window.add_new_overlay(overlay)
        self.window.show_overlay(overlay)

    def eventItemOverlayPathObject(self, action: Action, *args):
        self.window.dismiss_all()
        if action == Action.OPEN:
            item = args[0]
            self.get_func_action_click_path_object(item)(item)
        elif action == Action.DELETE:
            item = args[0]
            delete_overlay = QActionDeletePathObject(item, self.window,
                                                     lambda obj: self.click_action_delete_ok(delete_overlay, obj),
                                                     lambda obj: self.click_action_cancel_overlay(delete_overlay))
            self.window.add_new_overlay(delete_overlay)
            self.window.show_overlay(delete_overlay)
        elif action == Action.RENAME:
            item = args[0]
            rename_overlay = QActionRenamePathObject(
                self.window, item,
                positive=lambda new_name, obj: self.click_action_rename(rename_overlay, new_name, obj),
                negative=lambda obj: self.click_action_cancel_overlay(rename_overlay)
            )
            self.window.add_new_overlay(rename_overlay)
            self.window.show_overlay(rename_overlay)
        elif action == Action.CREATE_FILE or action == Action.CREATE_FOLDER:
            txt = f"Введите название для {'нового файла' if Action.CREATE_FILE else 'новой папки'}"
            type_obj = TypePathObject.FILE if action == Action.CREATE_FILE else TypePathObject.FOLDER
            set_name = QActionLineEdit(self.window, txt)
            set_name.set_negative("Отмена", lambda: self.window.dismiss_parent(set_name))
            set_name.set_positive("Готово", lambda name: self.click_action_create_path_object(set_name, name, type_obj))
            self.window.add_new_overlay(set_name)
            self.window.show_overlay(set_name)
        elif action == Action.PRE_OPEN:
            item = args[0]
            widget = self.get_widget_path_object(item)
            x = widget.x() + widget.width() // 2
            y = widget.y() + widget.height() // 2
            preview = PreviewsFactory.get_preview_path_object(x, y, self.window, item)
            self.preview_manager.show_preview(preview)
        elif action == Action.OPEN_NEW_TAB:
            item = args[0]
            self.on_new_tab(item)
        elif action == Action.ADD_FAVORITE:
            item = args[0]
            self.db_manager.favorites.add_favorite(item.path)
            self.on_change_favorite(item)
        elif action == Action.REMOVE_FAVORITE:
            item = args[0]
            self.db_manager.favorites.remove_favorite(item.path)
            self.on_change_favorite(item)

    def click_action_create_path_object(self, overlay: QOverlay,
                                        new_name: str,
                                        type_obj: TypePathObject = TypePathObject.FILE):
        if not self._tab.folder.check_exist_child(new_name):
            if type_obj == TypePathObject.FILE:
                self._tab.folder.create_child_file(new_name)
            if type_obj == TypePathObject.FOLDER:
                self._tab.folder.create_child_folder(new_name)
            self.window.dismiss_parent(overlay)
            self.refresh_content()
        else:
            message = QActionAlertDialog(f"{type_obj.to_rus_str()} с таким именем уже создан", self.window)
            self.window.add_new_overlay(message)
            self.window.show_overlay(message)

    def click_action_rename(self, overlay: QActionRenamePathObject, new_name: str, obj: PathObject):
        self.rename_path_object(new_name, obj)
        self.window.dismiss_parent(overlay)

    def click_action_delete_ok(self, overlay: QActionDeletePathObject, obj: PathObject):
        self.window.dismiss_parent(overlay)
        self.remove_path_object(obj)

    def remove_path_object(self, path_object: PathObject):
        path_object.delete()
        self._tab.folder.refresh()
        self.refresh_content()

    def get_widget_path_object(self, path_object: PathObject) -> QWidget:
        for widget in [j for i in self.widgets for j in i]:
            if widget.obj == path_object:
                return widget
        raise ValueError(f"Widget for {path_object} in MainAreaWindow not found")

    def click_action_cancel_overlay(self, overlay: QOverlay):
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

    def refresh_content(self):
        self.clear()
        self._tab.folder.refresh()
        [self.add_item_path_object(i) for i in self._tab.folder.children]
        if not self._tab.folder.exist_permissions():
            self.window.show_error(str(f"Отказ в доступе '{self._tab.folder.path}'"))

    def set_tab(self, tab: Tab):
        self._tab = tab
        self._tab.add_on_change_folder(lambda last_folder, x: self.refresh_content())
        self.refresh_content()

    def get_tab(self):
        return self._tab

    def rename_path_object(self, new_name, obj: PathObject):
        obj.rename(self._tab.folder.add_to_path(new_name))
        self._tab.folder.refresh()
        self.refresh_content()

    def mousePressEvent(self, event: QMouseEvent):
        menu_overlay = QActionMenu(event.x(), event.y(), self.window,
                                   [Action.CREATE_FILE, Action.CREATE_FOLDER])
        menu_overlay.clickItemEvent = self.eventItemOverlayPathObject
        self.window.add_new_overlay(menu_overlay)
        self.window.show_overlay(menu_overlay)
