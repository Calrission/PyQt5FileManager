from areas.WindowArea import WindowArea
from managers.OverlayManager import QWidgetOverlayManager
from values.Areas import Areas
from values.ConstValues import START_X_SETTING, START_Y_BUTTON, START_X_HISTORY_BUTTON, MARGIN_BUTTON_HISTORY, \
    WIDTH_BUTTON
from values.TypeImageButton import TypeImageButton
from widgets.QSwitchImageButton import QSwitchImageButton


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