# -*- coding: utf-8 -*-

from libs.common import *
from libs.constants import *


class Fonts:
    def __init__(self, constants: Constants):
        font_size = int(round(constants.playing_area_right / 14))
        self.main_menu_item = pg.font.Font(
            Common.get_script_path() + '/fonts/gabo___free_elegant_font_by_dannci_d2m28g9.otf', font_size)

        font_size = int(round(constants.playing_area_right / 8))
        self.game_over = pg.font.Font(
            Common.get_script_path() + '/fonts/gabo___free_elegant_font_by_dannci_d2m28g9.otf', font_size)

        font_size = int(round(constants.playing_area_right / 8))
        self.level_number = pg.font.Font(
            Common.get_script_path() + '/fonts/gabo___free_elegant_font_by_dannci_d2m28g9.otf',
            font_size)

        font_size = int(round(constants.playing_area_right / 8))
        self.sidebar_level = pg.font.Font(
            Common.get_script_path() + '/fonts/gabo___free_elegant_font_by_dannci_d2m28g9.otf', font_size)

        font_size = int(round(constants.playing_area_right / 16))
        self.sidebar_points = pg.font.Font(
            Common.get_script_path() + '/fonts/gabo___free_elegant_font_by_dannci_d2m28g9.otf',
            font_size)

        font_size = int(round(constants.playing_area_right / 8))
        self.game_paused_title = pg.font.Font(
            Common.get_script_path() + '/fonts/gabo___free_elegant_font_by_dannci_d2m28g9.otf',
            font_size)

        font_size = int(round(constants.playing_area_right / 12))
        self.game_paused_press_key = pg.font.Font(
            Common.get_script_path() + '/fonts/gabo___free_elegant_font_by_dannci_d2m28g9.otf',
            font_size)
