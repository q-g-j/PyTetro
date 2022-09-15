# -*- coding: utf-8 -*-

import pygame as pg


class Constants:
    def __init__(self):
        self.fps = 60

        self.max_level = 20
        self.lines_needed_for_first_level_up = 10

        self.level_diff_tetromino_move_down_ms = 25
        self.level_diff_tetromino_at_bottom_ms = 15
        self.level_diff_drop_tetrominoes_ms = 15
        self.level_diff_has_lost_ms = 15

        self.delay_print_game_over_ms = 5000

        self.block_size, self.window_width, self.window_height = self.__calc_sizes()
        self.block_inner_rect_offset_x = int(round(self.block_size / 8))
        self.block_inner_rect_offset_y = self.block_inner_rect_offset_x
        self.block_inner_rect_width = self.block_size - self.block_inner_rect_offset_x * 2
        self.block_inner_rect_height = self.block_inner_rect_width
        self.sidebar_left = self.window_width
        self.playing_area_top = 0
        self.playing_area_left = self.block_size
        self.playing_area_right = self.window_width - self.block_size
        self.playing_area_bottom = self.window_height - self.block_size
        self.sidebar_factor = 1.5
        self.window_width_total = int(self.window_width * self.sidebar_factor)
        self.sidebar_width = self.window_width_total - self.window_width

    @staticmethod
    def __calc_sizes() -> tuple[int, int, int]:
        window_height = int(round(pg.display.Info().current_h * (2 / 3)))
        block_size = int(round(window_height / 22))
        if block_size % 2 == 0:
            block_size += 1
        window_width = block_size * 14
        window_height = block_size * 22
        return block_size, window_width, window_height
