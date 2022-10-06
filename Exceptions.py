class NotFolderException(Exception):
    def __init__(self, directory_path):
        super(NotFolderException, self).__init__(f"Это не директория:\n{directory_path}")


class NotFileException(Exception):
    def __init__(self, directory_file):
        super(NotFileException, self).__init__(f"Это не файл:\n{directory_file}")


class DetectFormatFileError(Exception):
    def __init__(self, file):
        super(DetectFormatFileError, self).__init__(f"Ошибка взятия формата у файла:\n{file}")


class EmptyDetectFormatFileError(Exception):
    def __init__(self, file):
        super(EmptyDetectFormatFileError, self).__init__(f"Пустой формат у файла:\n{file}")


class DetectNameFromPathError(Exception):
    def __init__(self, file):
        super(DetectNameFromPathError, self).__init__(f"Не удалось получить имя из пути файла:\n{file}")


class MovingToFolderError(Exception):
    def __init__(self, start_folder, to_folder):
        super(MovingToFolderError, self).__init__(f"Не удалось перейти в под папку:\n{start_folder} -> {to_folder}")


class GetFileFolderError(Exception):
    def __init__(self, file, folder):
        super(GetFileFolderError, self).__init__(f"Не удалось получить файл в папке:\n{file} в {folder}")