from PathObjects import *
from Tab import Tab
from pprint import pprint

tab = Tab("/home/artemii/Загрузки")
while True:
    content = [str(i) for i in tab.folder.children]
    pprint(content)
    obj = input("Введите название объекта: ")
    if obj == "back":
        tab.move_back_history()
        continue
    if obj == "next":
        tab.move_next_history()
        continue
    path_obj = tab.folder.get_child(obj)
    if isinstance(path_obj, File):
        path_obj.open_default_app_os()
    elif isinstance(path_obj, Folder):
        tab.move_to_child_folder(path_obj.name)
