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

START_Y_TP = 5
END_Y_TP = 30
START_Y_MP = END_Y_TP
START_Y_LP = END_Y_TP
END_Y_LP = HEIGHT
START_X_LP = 0
END_X_LP = 180
START_X_MP = END_X_LP
END_X_MP = WIDTH
START_X_TP = 0
END_X_TP = WIDTH
END_Y_MP = HEIGHT

WIDTH_TP = END_X_TP - START_X_TP
HEIGHT_TP = END_Y_TP - START_Y_TP

WIDTH_LP = END_X_LP - START_X_LP
HEIGHT_LP = END_Y_LP - START_Y_LP

WIDTH_MP = END_X_MP - START_X_MP
HEIGHT_MP = END_Y_MP - START_Y_MP
