# -*- coding: utf-8 -*-

import pygame as pg
from libs.constants import *
from libs.colors import *


class FrameBlock(pg.sprite.Sprite):
    def __init__(self, _screen):
        super(FrameBlock, self).__init__()
        self.mask = None
        self.draw()

    def draw(self):
        self.image = pg.Surface((TETROMINO_SIZE, TETROMINO_SIZE))
        self.rect = self.image.get_rect()

        pg.draw.polygon(surface=self.image, color=Colors.FrameBlock.bg_topleft,
                        points=[(0, TETROMINO_SIZE - 1),
                                (0, 0),
                                (TETROMINO_SIZE - 1, 0)])
        pg.draw.polygon(surface=self.image, color=Colors.FrameBlock.bg_bottomright,
                        points=[(0, TETROMINO_SIZE - 1),
                                (TETROMINO_SIZE - 1, 0),
                                (TETROMINO_SIZE - 1, TETROMINO_SIZE - 1)])
        pg.draw.rect(self.image,
                     color=Colors.FrameBlock.fg_square,
                     rect=(int(TETROMINO_SIZE / 8),
                           int(TETROMINO_SIZE / 8),
                           int(TETROMINO_SIZE / (4 / 3)),
                           int(TETROMINO_SIZE / (4 / 3))))

        self.image.set_colorkey(Colors.BLACK)
        self.mask = pg.mask.from_surface(self.image)
