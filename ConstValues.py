MAX_WIDTH = 800
MAX_HEIGHT = 600
MIN_WIDTH = MAX_WIDTH
MIN_HEIGHT = MAX_HEIGHT
HEIGHT = MAX_HEIGHT
WIDTH = MAX_WIDTH
TITLE = "Файлики и папочки"

# TP (TabPanel) - верхняя панель для вкладок
# MP (MainPanel) - панель для файлов и папок
# LP (LeftPanel) - левая панель


MARGIN_TAB_V_TP = 5
MARGIN_TAB_H_TP = 5
HEIGHT_TAB_TP = 30

PADDING_TAB = 5

START_Y_PANEL_HISTORY = 0
START_X_PANEL_HISTORY = 0

START_Y_TP = 0
END_Y_TP = 2 * MARGIN_TAB_V_TP + HEIGHT_TAB_TP
START_Y_MP = END_Y_TP
START_Y_LP = END_Y_TP
END_Y_LP = HEIGHT
START_X_LP = 0
END_X_LP = 180
START_X_MP = END_X_LP
END_X_MP = WIDTH

END_X_TP = WIDTH
END_Y_MP = HEIGHT

HEIGHT_TP = END_Y_TP - START_Y_TP

MARGIN_BUTTON_HISTORY = MARGIN_TAB_V_TP

WIDTH_HISTORY_BUTTON = HEIGHT_TAB_TP
HEIGHT_HISTORY_BUTTON = WIDTH_HISTORY_BUTTON
HEIGHT_PANEL_HISTORY = HEIGHT_TP

END_X_PANEL_HISTORY = START_X_PANEL_HISTORY + 2 * WIDTH_HISTORY_BUTTON + 2 * MARGIN_BUTTON_HISTORY
END_Y_PANEL_HISTORY = END_Y_TP

WIDTH_PANEL_HISTORY = END_X_PANEL_HISTORY - START_X_PANEL_HISTORY

START_X_TP = WIDTH_PANEL_HISTORY

START_X_HISTORY_BUTTON = START_X_PANEL_HISTORY + MARGIN_BUTTON_HISTORY
START_Y_HISTORY_BUTTON = START_Y_PANEL_HISTORY + MARGIN_BUTTON_HISTORY

WIDTH_TP = END_X_TP - START_X_TP

WIDTH_LP = END_X_LP - START_X_LP
HEIGHT_LP = END_Y_LP - START_Y_LP

WIDTH_MP = END_X_MP - START_X_MP
HEIGHT_MP = END_Y_MP - START_Y_MP

WIDTH_ITEM = 93
HEIGHT_ITEM = 95
MARGIN_ITEM = 10
WIDTH_ICON = 50
HEIGHT_ICON = WIDTH_ICON
WIDTH_TEXT = WIDTH_ITEM
HEIGHT_TEXT = HEIGHT_ITEM - HEIGHT_ICON
MAX_LINE_TEXT = 12

FONT_SIZE = 10

ANGLE_WHEEL_TO_PX = 0.3

COLOR_BACKGROUND_TOP_RGB = (24, 24, 24)
COLOR_BACKGROUND_DEFAULT = (0, 0, 0)
COLOR_BACKGROUND_LEFT_RGB = (16, 16, 16)
COLOR_BACKGROUND_MAIN_RGB = (0, 0, 0)
COLOR_RED_TEST_RDB = (255, 0, 0)

COLOR_TEXT = (255, 255, 255)

TXT_FORMATS = ["txt", "csv"]
VIDEO_FORMATS = ["mp4"]
ARCHIVE_FORMATS = ["zip"]
PYTHON_FORMATS = ["py"]
WORD_FORMATS = ["docx", "doc"]
TORRENT_FORMATS = ["torrent"]
AUDIO_FORMATS = ["mp3"]
PYTHON_BYTECODE_FORMATS = ["pyc"]
IMAGE_FORMATS = ["png", "jpeg", "jpg", "bmp"]
EXCEL_FORMATS = ["xlsx", "xlsm", "xltx", "xlt",
                 "xlsb", "xlam", "xltm", "xla"
                                         "xls"]
PDF_FORMATS = ["pdf", "psd", "psb"]
PHOTOSHOP = []
JAVA_FORMATS = ["java"]
JAR_FORMATS = ["jar"]
POWERPOINT_FORMATS = ["ppxt", "pptm", "ppt", "potx",
                      "pot", "potm"]
QT_UI_FORMATS = ["ui"]
APK_FORMATS = ["apk"]

OS = "unknown"

SLASH_WINDOWS = "\\"
SLASH_LINUX = "/"
SLASH = ""


def initSLASH():
    global SLASH
    if OS != "Darwin":
        if OS == "Windows":
            SLASH = SLASH_WINDOWS
        else:
            SLASH = SLASH_LINUX
