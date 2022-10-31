import os
import shutil
from os.path import exists
from os import listdir
from Exceptions import *
from enum import Enum
from ConstValues import SLASH, OS, START_TAB, AUDIO_FORMATS, VIDEO_FORMATS, IMAGE_FORMATS, \
    TXT_FORMATS, CODE_FORMATS, PDF_FORMATS, WORD_FORMATS, EXCEL_FORMATS, POWERPOINT_FORMATS


class TypePathObject(Enum):
    FOLDER = "folder"
    FILE = "file"
    UNKNOWN = "unknown"


class TypeFormatFile(Enum):
    MEDIA = "media"
    TXT = "txt"
    CODE = "code"
    OFFICE = "office"
    OTHER = "other"


class PathObject:
    def __init__(self, path: str, name: str = None):
        self.path = path
        self.name = name
        if name is None:
            self._detect_name_from_path()
        else:
            self.path += f"{SLASH}{self.name}"
        self.type = TypePathObject.UNKNOWN
        self.__detect_type()

    def __detect_type(self):
        if os.path.isfile(self.path):
            self.type = TypePathObject.FILE
        elif os.path.isdir(self.path):
            self.type = TypePathObject.FOLDER
        else:
            self.type = TypePathObject.UNKNOWN

    def _detect_name_from_path(self):
        try:
            self.name = self.path[::-1][:self.path[::-1].index(SLASH)][::-1]
        except ValueError:
            raise DetectNameFromPathError(self)

    def check_exist(self):
        return exists(self.path)

    def refresh(self):
        pass

    def delete(self):
        pass

    def rename(self, new_name: str):
        os.rename(self.path, new_name)

    def __repr__(self):
        return f"{self.__class__.__name__}; {self.path}; {self.type}; "

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def check_exist_path(path: str):
        return os.path.exists(path)


class Folder(PathObject):
    def __init__(self, path: str, name: str = None):
        self.children = []
        self.children_folders = []
        self.children_files = []
        if path == "":
            path = START_TAB
        if path[-1] == SLASH and path != START_TAB:
            path = path[:-1]
        super().__init__(path, name)
        if self.name is None:
            self._detect_name_from_path()

    def delete(self):
        shutil.rmtree(self.path)

    def __check_type(self):
        if self.type != TypePathObject.FOLDER:
            raise NotFolderException(self)

    def exist_permissions(self):
        try:
            listdir(self.path)
            return True
        except PermissionError:
            return False

    def refresh(self):
        self.__check_type()
        self.__detect_children()

    def get_parent_folder_path(self):
        if self.path == SLASH:
            return None
        return SLASH.join(self.path.split(SLASH)[:-1])

    def __detect_children(self):
        try:
            lst = listdir(self.path)
        except PermissionError:
            lst = []
        folders = [Folder(self.path, folder) for folder in lst if self.isdir(folder)]
        files = [File(self.path, file) for file in lst if self.isfile(file)]
        self._set_content(folders + files, folders, files)

    def _set_content(self, children: list, folders: list, files: list):
        self.children = children
        self.children_folders = folders
        self.children_files = files

    def get_file(self, file_name):
        try:
            return [i for i in self.children_files if i.name == file_name][0]
        except IndexError:
            raise GetFileFolderError(file_name, self)

    def get_child(self, obj: str):
        try:
            return [i for i in self.children if i.name == obj][0]
        except IndexError:
            raise GetFileFolderError(obj, self)

    def __str__(self):
        return self.path

    def __repr__(self):
        return super().__repr__() + f"{len(self.children)};"

    def next(self, next_folder_name: str):
        try:
            self.__init__(self.path + f"{SLASH if self.path != START_TAB else ''}{next_folder_name}")
        except IndexError:
            raise MovingToFolderError(self, next_folder_name)

    def change(self, new_folder_path: str):
        self.__init__(new_folder_path)

    def change_path(self, new_path: str):
        self.__init__(new_path)

    def isdir(self, obj_name):
        res = os.path.isdir(self.add_to_path(obj_name))
        return res

    def isfile(self, obj_file):
        return os.path.isfile(self.add_to_path(obj_file))

    def add_to_path(self, obj_name):
        return self.path + SLASH + obj_name

    def get_short_name(self):
        # 1/2/3/4 -> 3/4
        short = self.path
        if short.replace(START_TAB, SLASH).count(SLASH) >= 2:
            short = SLASH.join(short.split(SLASH)[-2:])
        return short

    def create_child_folder(self, folder_name: str):
        new_folder_path = self.add_to_path(folder_name)
        if not PathObject.check_exist(new_folder_path):
            os.makedirs(new_folder_path)

    def create_child_file(self, file_name: str):
        new_file_path = self.add_to_path(file_name)
        if not PathObject.check_exist_path(new_file_path):
            open(new_file_path, 'a').close()

    def check_exist_child(self, child_name: str):
        return child_name in [str(i.name) for i in self.children]


class File(PathObject):
    def __init__(self, path: str, name: str = None):
        self.format = ""
        super().__init__(path, name)
        self.refresh()

    def __check_type(self):
        if self.type != TypePathObject.FILE:
            raise NotFileException(self)

    def __detect_format(self):
        try:
            r = self.name[::-1]
            self.format = r[:r.index(".")][::-1]
        except ValueError:
            self.format = ""

    def __detect_type_file(self):
        pass

    def open_default_app_os(self):
        if OS == 'Darwin':  # macOS not support
            pass
            # from subprocess import call
            # call(('open', self.path))
        if OS == 'Windows':  # Windows
            from os import startfile
            startfile(self.path)
        else:  # linux variants
            from subprocess import call
            call(('xdg-open', self.path))

    def get_type_format(self):
        if self.format in IMAGE_FORMATS + VIDEO_FORMATS + AUDIO_FORMATS:
            return TypeFormatFile.MEDIA
        if self.format in PDF_FORMATS + WORD_FORMATS + POWERPOINT_FORMATS + EXCEL_FORMATS:
            return TypeFormatFile.OFFICE
        if self.format in CODE_FORMATS:
            return TypeFormatFile.CODE
        if self.format in TXT_FORMATS:
            return TypeFormatFile.TXT
        return TypeFormatFile.OTHER

    def refresh(self):
        self.__check_type()
        self.__detect_format()
        self.__detect_type_file()

    def delete(self):
        os.remove(self.path)

    def __repr__(self):
        return super().__repr__() + f"{self.format};"

    def __str__(self):
        return self.name
