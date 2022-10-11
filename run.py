from PathObjects import *
from Tab import Tab
from pprint import pprint
from PyQt5.QtWidgets import QApplication
from App import Main
from sys import argv, exit
from platform import system


def startTerminalVersion():
    tab = Tab("")
    while True:
        content = [str(i) for i in tab.folder.children]
        pprint(content)
        obj = input("Введите название объекта: ")
        if obj == "back":
            tab.move_prev_history()
            continue
        if obj == "next":
            tab.move_next_history()
            continue
        try:
            path_obj = tab.folder.get_child(obj)
            if isinstance(path_obj, File):
                path_obj.open_default_app_os()
            elif isinstance(path_obj, Folder):
                tab.move_to_child_folder(path_obj.name)
        except GetFileFolderError:
            print("Error")


if __name__ == "__main__":
    if len(argv) >= 2 and argv[1] == "-t":
        startTerminalVersion()
    app = QApplication(argv)
    main = Main()
    main.show()
    exit(app.exec())
