# -*- coding: utf-8 -*-

import pygame as pg

from libs.common import *


class Fonts:
    def __init__(self):
        self.game_over = pg.font.Font(
            Common.get_script_path() + '/fonts/gabo___free_elegant_font_by_dannci_d2m28g9.otf', 60)
