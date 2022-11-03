from enum import Enum


class TypePathObject(Enum):
    FOLDER = "folder"
    FILE = "file"
    UNKNOWN = "unknown"

    def to_rus_str(self):
        if self == TypePathObject.FOLDER:
            return "Папка"
        elif self == TypePathObject.FILE:
            return "Файл"
        return self.value
