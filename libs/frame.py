# -*- coding: utf-8 -*-

import pygame as pg
import libs.colors as colors


class Frame:
    def __init__(self, _constants, _all_sprites):
        self.__constants = _constants
        self.__all_sprites = _all_sprites

    def create_frame(self):
        for i in range(0, int(self.__constants.playing_area_right / self.__constants.block_size) + self.__constants.block_size):
            frame_block = FrameBlock(self.__constants)
            frame_block.rect.x = i * self.__constants.block_size
            frame_block.rect.y = -self.__constants.block_size
            self.__all_sprites.add(frame_block)
        for i in range(0, int(self.__constants.playing_area_right / self.__constants.block_size) + self.__constants.block_size):
            frame_block = FrameBlock(self.__constants)
            frame_block.rect.x = i * self.__constants.block_size
            frame_block.rect.y = 21 * self.__constants.block_size + self.__constants.block_size
            self.__all_sprites.add(frame_block)
        for i in range(0, 22):
            frame_block = FrameBlock(self.__constants)
            frame_block.rect.x = 0
            frame_block.rect.y = i * self.__constants.block_size
            self.__all_sprites.add(frame_block)
        for i in range(0, 22):
            frame_block = FrameBlock(self.__constants)
            frame_block.rect.x = int(self.__constants.playing_area_right / self.__constants.block_size) \
                * self.__constants.block_size
            frame_block.rect.y = i * self.__constants.block_size
            self.__all_sprites.add(frame_block)


class FrameBlock(pg.sprite.Sprite):
    def __init__(self, _constants):
        super(FrameBlock, self).__init__()
        self.__constants = _constants
        self.mask = None
        self.draw()

    def draw(self):
        self.image = pg.Surface((self.__constants.block_size, self.__constants.block_size))
        self.rect = self.image.get_rect()

        pg.draw.polygon(surface=self.image, color=colors.Frame.FrameBlock.bg_topleft,
                        points=[(0, self.__constants.block_size - 1),
                                (0, 0),
                                (self.__constants.block_size - 1, 0)])
        pg.draw.polygon(surface=self.image, color=colors.Frame.FrameBlock.bg_bottomright,
                        points=[(0, self.__constants.block_size - 1),
                                (self.__constants.block_size - 1, 0),
                                (self.__constants.block_size - 1, self.__constants.block_size - 1)])
        pg.draw.rect(self.image,
                     color=colors.Frame.FrameBlock.fg_square,
                     rect=(int(round(self.__constants.block_size / 8)),
                           int(round(self.__constants.block_size / 8)),
                           int(round(self.__constants.block_size / (4 / 3))),
                           int(round(self.__constants.block_size / (4 / 3)))))

        self.image.set_colorkey(colors.Constants.BLACK)
        self.mask = pg.mask.from_surface(self.image)
