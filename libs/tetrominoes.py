# -*- coding: utf-8 -*-

from __future__ import annotations
import pygame as pg
from typing import Type

from libs.constants import Constants
import libs.colors as colors


class Tetromino(pg.sprite.Sprite):
    def __init__(self, _window: pg.Surface, _constants: Constants, _all_sprites: pg.sprite.Group,
                 _color: Type[colors.TetrominoBase]):
        super().__init__()
        self.window = _window
        self.constants = _constants
        self.all_sprites = _all_sprites
        self.color = _color

        self.shapes = []
        self.current_shape = 0
        self.mask = None

    def draw(self):
        num_blocks_hori = len(self.shapes[self.current_shape][0])
        num_blocks_verti = len(self.shapes[self.current_shape])

        self.image = pg.Surface((num_blocks_hori * self.constants.block_size,
                                 num_blocks_verti * self.constants.block_size))

        for j in range(num_blocks_verti):
            for i in range(num_blocks_hori):
                if self.shapes[self.current_shape][j][i]:
                    pg.draw.polygon(
                        surface=self.image, color=self.color.bg_topleft,
                        points=[(i * self.constants.block_size,
                                 (self.constants.block_size - 1) + j * self.constants.block_size),
                                (i * self.constants.block_size,
                                 j * self.constants.block_size),
                                ((self.constants.block_size - 1) + i * self.constants.block_size,
                                 j * self.constants.block_size)]
                    )
                    pg.draw.polygon(
                        surface=self.image, color=self.color.bg_bottomright,
                        points=[(i * self.constants.block_size,
                                 (self.constants.block_size - 1) + j * self.constants.block_size),
                                ((self.constants.block_size - 1) + i * self.constants.block_size,
                                 j * self.constants.block_size),
                                ((self.constants.block_size - 1) + i * self.constants.block_size,
                                 (self.constants.block_size - 1) + j * self.constants.block_size)]
                    )
                    pg.draw.rect(self.image,
                                 color=self.color.fg_square,
                                 rect=(self.constants.block_inner_rect_offset_x + i * self.constants.block_size,
                                       self.constants.block_inner_rect_offset_y + j * self.constants.block_size,
                                       self.constants.block_inner_rect_width,
                                       self.constants.block_inner_rect_height))

        self.image.set_colorkey(colors.Constants.BLACK)
        self.mask = pg.mask.from_surface(self.image)

    def __rotate(self, _direction: str):
        if _direction == 'left':
            self.current_shape = self.current_shape - 1 if self.current_shape > 0 else 3
        else:
            self.current_shape = self.current_shape + 1 if self.current_shape < 3 else 0

        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.constants.block_size,
                                 len(self.shapes[self.current_shape]) * self.constants.block_size))
        self.draw()

    def rotate_left(self):
        self.__rotate('left')
        if self.rect.y > self.constants.playing_area_bottom - self.image.get_height() or \
                self.rect.x < self.constants.playing_area_left or \
                self.rect.x > self.constants.playing_area_right - self.image.get_width():
            self.__rotate('right')
        else:
            colliding_sprite = self.does_collide(self.all_sprites)
            if colliding_sprite is not None:
                self.__rotate('right')

    def rotate_right(self):
        self.__rotate('right')
        if self.rect.y > self.constants.playing_area_bottom - self.image.get_height() or \
                self.rect.x < self.constants.playing_area_left or \
                self.rect.x > self.constants.playing_area_right - self.image.get_width():
            self.__rotate('left')
        else:
            colliding_sprite = self.does_collide(self.all_sprites)
            if colliding_sprite is not None:
                self.__rotate('left')

    def move_left(self):
        self.rect.x -= self.constants.block_size
        colliding_sprite = self.does_collide(self.all_sprites)
        if colliding_sprite is not None:
            self.rect.x += self.constants.block_size

    def move_right(self):
        self.rect.x += self.constants.block_size
        colliding_sprite = self.does_collide(self.all_sprites)
        if colliding_sprite is not None:
            self.rect.x -= self.constants.block_size

    def move_down(self):
        self.rect.y += self.constants.block_size

    def is_bottom(self) -> bool:
        if self.rect.y == self.constants.playing_area_bottom - self.image.get_height():
            return True
        return False

    def does_collide(self, _sprite_group: pg.sprite.Group) -> pg.sprite.Sprite | None:
        for t in _sprite_group:
            if t == self:
                continue
            if pg.sprite.collide_mask(self, t) is not None:
                return t
        return None

    def would_collide_down(self, _sprite_group: pg.sprite.Group) -> bool:
        self.rect.y += self.constants.block_size
        colliding_sprite = self.does_collide(_sprite_group)
        if colliding_sprite is not None:
            self.rect.y -= self.constants.block_size
            return True
        self.rect.y -= self.constants.block_size
        return False

    def would_collide_left(self, _sprite_group: pg.sprite.Group) -> bool:
        self.rect.x -= self.constants.block_size
        colliding_sprite = self.does_collide(_sprite_group)
        if colliding_sprite is not None:
            self.rect.x += self.constants.block_size
            return True
        self.rect.x += self.constants.block_size
        return False

    def would_collide_right(self, _sprite_group: pg.sprite.Group) -> bool:
        self.rect.x += self.constants.block_size
        colliding_sprite = self.does_collide(_sprite_group)
        if colliding_sprite is not None:
            self.rect.x -= self.constants.block_size
            return True
        self.rect.x -= self.constants.block_size
        return False


class SingleBlock(Tetromino):
    def __init__(self, _window: pg.Surface, _constants: Constants, _all_sprites: pg.sprite.Group, _color):
        super().__init__(_window, _constants, _all_sprites, _color)
        self.shapes = [
            [
                [1]
            ]
        ]
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.constants.block_size,
                                 len(self.shapes[self.current_shape]) * self.constants.block_size))
        self.rect = self.image.get_rect()
        self.draw()

    def rotate_left(self):
        pass

    def rotate_right(self):
        pass


class Straight(Tetromino):
    def __init__(self, _window: pg.Surface, _constants: Constants, _all_sprites: pg.sprite.Group):
        super().__init__(_window, _constants, _all_sprites, colors.TetrominoStraight)
        self.shapes = [
            [
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0]
            ],
            [
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],
            [
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0]
            ]
        ]
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.constants.block_size,
                                 len(self.shapes[self.current_shape]) * self.constants.block_size))
        self.rect = self.image.get_rect()
        self.draw()


class Square(Tetromino):
    def __init__(self, _window: pg.Surface, _constants: Constants, _all_sprites: pg.sprite.Group):
        super().__init__(_window, _constants, _all_sprites, colors.TetrominoSquare)
        self.shapes = [
            [
                [1, 1],
                [1, 1]
            ]
        ]
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.constants.block_size,
                                 len(self.shapes[self.current_shape]) * self.constants.block_size))
        self.rect = self.image.get_rect()
        self.draw()

    def rotate_left(self):
        pass

    def rotate_right(self):
        pass


class T(Tetromino):
    def __init__(self, _window: pg.Surface, _constants: Constants, _all_sprites: pg.sprite.Group):
        super().__init__(_window, _constants, _all_sprites, colors.TetrominoT)
        self.shapes = [
            [
                [1, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 0, 1],
                [0, 1, 1],
                [0, 0, 1]
            ],
            [
                [0, 0, 0],
                [0, 1, 0],
                [1, 1, 1]
            ],
            [
                [1, 0, 0],
                [1, 1, 0],
                [1, 0, 0]
            ]
        ]
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.constants.block_size,
                                 len(self.shapes[self.current_shape]) * self.constants.block_size))
        self.rect = self.image.get_rect()
        self.draw()


class L(Tetromino):
    def __init__(self, _window: pg.Surface, _constants: Constants, _all_sprites: pg.sprite.Group):
        super().__init__(_window, _constants, _all_sprites, colors.TetrominoL)
        self.shapes = [
            [
                [1, 0],
                [1, 0],
                [1, 1]
            ],
            [
                [1, 1, 1],
                [1, 0, 0]
            ],
            [
                [0, 1, 1],
                [0, 0, 1],
                [0, 0, 1]
            ],
            [
                [0, 0, 0],
                [0, 0, 1],
                [1, 1, 1]
            ]
        ]
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.constants.block_size,
                                 len(self.shapes[self.current_shape]) * self.constants.block_size))
        self.rect = self.image.get_rect()
        self.draw()


class J(Tetromino):
    def __init__(self, _window: pg.Surface, _constants: Constants, _all_sprites: pg.sprite.Group):
        super().__init__(_window, _constants, _all_sprites, colors.TetrominoJ)
        self.shapes = [
            [
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 1, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 0, 0],
                [1, 1, 1]
            ],
            [
                [1, 1],
                [1, 0],
                [1, 0]
            ],
            [
                [1, 1, 1],
                [0, 0, 1],
                [0, 0, 0]
            ]
        ]
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.constants.block_size,
                                 len(self.shapes[self.current_shape]) * self.constants.block_size))
        self.rect = self.image.get_rect()
        self.draw()


class S(Tetromino):
    def __init__(self, _window: pg.Surface, _constants: Constants, _all_sprites: pg.sprite.Group):
        super().__init__(_window, _constants, _all_sprites, colors.TetrominoS)
        self.shapes = [
            [
                [0, 1, 1],
                [1, 1, 0],
            ],
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 0, 1]
            ],
            [
                [0, 0, 0],
                [0, 1, 1],
                [1, 1, 0],
            ],
            [
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]
        ]
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.constants.block_size,
                                 len(self.shapes[self.current_shape]) * self.constants.block_size))
        self.rect = self.image.get_rect()
        self.draw()


class Z(Tetromino):
    def __init__(self, _window: pg.Surface, _constants: Constants, _all_sprites: pg.sprite.Group):
        super().__init__(_window, _constants, _all_sprites, colors.TetrominoZ)
        self.shapes = [
            [
                [1, 1, 0],
                [0, 1, 1],
            ],
            [
                [0, 0, 1],
                [0, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 0, 0],
                [1, 1, 0],
                [0, 1, 1]
            ],
            [
                [0, 1],
                [1, 1],
                [1, 0]
            ]
        ]
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.constants.block_size,
                                 len(self.shapes[self.current_shape]) * self.constants.block_size))
        self.rect = self.image.get_rect()
        self.draw()
