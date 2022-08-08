# -*- coding: utf-8 -*-

import pygame as pg
from libs.colors import *


class FrameBlock(pg.sprite.Sprite):
    def __init__(self, _screen, _tetromino_size):
        super(FrameBlock, self).__init__()
        self.tetromino_size = _tetromino_size
        self.mask = None
        self.draw()

    def draw(self):
        self.image = pg.Surface((self.tetromino_size, self.tetromino_size))
        self.rect = self.image.get_rect()

        pg.draw.polygon(surface=self.image, color=Colors.FrameBlock.bg_topleft,
                        points=[(0, self.tetromino_size - 1),
                                (0, 0),
                                (self.tetromino_size - 1, 0)])
        pg.draw.polygon(surface=self.image, color=Colors.FrameBlock.bg_bottomright,
                        points=[(0, self.tetromino_size - 1),
                                (self.tetromino_size - 1, 0),
                                (self.tetromino_size - 1, self.tetromino_size - 1)])
        pg.draw.rect(self.image,
                     color=Colors.FrameBlock.fg_square,
                     rect=(int(round(self.tetromino_size / 8)),
                           int(round(self.tetromino_size / 8)),
                           int(round(self.tetromino_size / (4 / 3))),
                           int(round(self.tetromino_size / (4 / 3)))))

        self.image.set_colorkey(Colors.BLACK)
        self.mask = pg.mask.from_surface(self.image)
