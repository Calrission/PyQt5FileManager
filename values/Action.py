from enum import Enum


class Action(Enum):
    OPEN = "Открыть"
    RENAME = "Переименовать"
    DELETE = "Удалить"
    PRE_OPEN = "Предпросмотр"
    INFO = "Свойства"
    CREATE_FOLDER = "Создать папку"
    CREATE_FILE = "Создать файл"
    OPEN_NEW_TAB = "Открыть в новой вкладке"
    CLOSE_TAB = "Закрыть вкладку"
    ADD_FAVORITE = "Добавить в избранное"
    REMOVE_FAVORITE = "Удалить из избранного"
