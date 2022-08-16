# -*- coding: utf-8 -*-

import pygame as pg


class Constants:
    def __init__(self):
        self.block_size, self.window_width, self.window_height = self.__compute_sizes()
        self.playing_area_top = 0
        self.playing_area_left = self.block_size
        self.playing_area_right = self.window_width - self.block_size
        self.playing_area_bottom = self.window_height - self.block_size

    @staticmethod
    def __compute_sizes():
        window_height = int(round(pg.display.Info().current_h * (2 / 3)))
        block_size = int(round(window_height / 22))
        if block_size % 2 == 0:
            block_size += 1
        window_width = block_size * 14
        window_height = block_size * 22
        return block_size, window_width, window_height
