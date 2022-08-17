# -*- coding: utf-8 -*-

import pygame as pg

from libs.common import *


class Fonts:
    def __init__(self, constants):
        font_size_menu_item = int(round(constants.playing_area_right / 14))
        self.main_menu_item = pg.font.Font(
            Common.get_script_path() + '/fonts/gabo___free_elegant_font_by_dannci_d2m28g9.otf', font_size_menu_item)

        font_size_game_over = int(round(constants.playing_area_right / 8))
        self.game_over = pg.font.Font(
            Common.get_script_path() + '/fonts/gabo___free_elegant_font_by_dannci_d2m28g9.otf', font_size_game_over)

        font_size_difficulty_number = int(round(constants.playing_area_right / 8))
        self.difficulty_number = pg.font.Font(
            Common.get_script_path() + '/fonts/gabo___free_elegant_font_by_dannci_d2m28g9.otf',
            font_size_difficulty_number)

        font_size_sidebar_level = int(round(constants.playing_area_right / 8))
        self.sidebar_level = pg.font.Font(
            Common.get_script_path() + '/fonts/gabo___free_elegant_font_by_dannci_d2m28g9.otf', font_size_sidebar_level)

        font_size_sidebar_points = int(round(constants.playing_area_right / 16))
        self.sidebar_points = pg.font.Font(
            Common.get_script_path() + '/fonts/gabo___free_elegant_font_by_dannci_d2m28g9.otf',
            font_size_sidebar_points)
