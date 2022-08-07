# -*- coding: utf-8 -*-

TETROMINO_SIZE = 35

SCREEN_WIDTH = TETROMINO_SIZE * 12 + 2 * TETROMINO_SIZE
SCREEN_HEIGHT = TETROMINO_SIZE * 20 + 2 * TETROMINO_SIZE

PLAYING_AREA_TOP = 0
PLAYING_AREA_LEFT = TETROMINO_SIZE
PLAYING_AREA_RIGHT = SCREEN_WIDTH - TETROMINO_SIZE
PLAYING_AREA_BOTTOM = SCREEN_HEIGHT - TETROMINO_SIZE
