# -*- coding: utf-8 -*-

import pygame as pg
from libs.colors import *


class Tetromino(pg.sprite.Sprite):
    def __init__(self, _screen, _playing_area_bottom, _playing_area_left,
                 _playing_area_right, _tetromino_size, _all_sprites, _color):
        super(Tetromino, self).__init__()
        self.playing_area_bottom = _playing_area_bottom
        self.playing_area_left = _playing_area_left
        self.playing_area_right = _playing_area_right
        self.tetromino_size = _tetromino_size
        self.shapes = list()
        self.shape_widths = list()
        self.shape_heights = list()
        self.current_shape = 0
        self.screen = _screen
        self.color = _color
        self.mask = None
        self.all_sprites = _all_sprites

    def draw(self):
        num_blocks_hori = len(self.shapes[self.current_shape][0])
        num_blocks_verti = len(self.shapes[self.current_shape])

        self.image = pg.Surface((num_blocks_hori * self.tetromino_size,
                                 num_blocks_verti * self.tetromino_size))

        for j in range(num_blocks_verti):
            for i in range(num_blocks_hori):
                if self.shapes[self.current_shape][j][i]:
                    pg.draw.polygon(
                        surface=self.image, color=self.color.bg_topleft,
                        points=[(0 + i * self.tetromino_size, (self.tetromino_size - 1) + j * self.tetromino_size),
                                (0 + i * self.tetromino_size, 0 + j * self.tetromino_size),
                                ((self.tetromino_size - 1) + i * self.tetromino_size, 0 + j * self.tetromino_size)]
                    )
                    pg.draw.polygon(
                        surface=self.image, color=self.color.bg_bottomright,
                        points=[(0 + i * self.tetromino_size,
                                 (self.tetromino_size - 1) + j * self.tetromino_size),
                                ((self.tetromino_size - 1) + i * self.tetromino_size,
                                 0 + j * self.tetromino_size),
                                ((self.tetromino_size - 1) + i * self.tetromino_size,
                                 (self.tetromino_size - 1) + j * self.tetromino_size)]
                    )
                    pg.draw.rect(self.image,
                                 color=self.color.fg_square,
                                 rect=(int(round(self.tetromino_size / 8)) + i * self.tetromino_size,
                                       int(round(self.tetromino_size / 8)) + j * self.tetromino_size,
                                       int(round(self.tetromino_size / (4 / 3))),
                                       int(round(self.tetromino_size / (4 / 3)))))

        self.image.set_colorkey(Colors.BLACK)
        self.mask = pg.mask.from_surface(self.image)

    def is_block_in_tetromino(self, rect):
        if self.rect.x + self.image.get_width() >= rect.x >= self.rect.x and \
                self.rect.y + self.image.get_height() >= rect.y >= self.rect.y:
            return True, self
        return False, self

    def __rotate(self, _direction):
        if _direction == 'left':
            self.current_shape = self.current_shape - 1 if self.current_shape > 0 else 3
        else:
            self.current_shape = self.current_shape + 1 if self.current_shape < 3 else 0

        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.tetromino_size,
                                 len(self.shapes[self.current_shape]) * self.tetromino_size))
        self.draw()

    def rotate_right(self):
        self.__rotate('right')
        if self.rect.y > self.playing_area_bottom - self.image.get_height() or \
                self.rect.x < self.playing_area_left or \
                self.rect.x > self.playing_area_right - self.image.get_width():
            self.__rotate('left')
        else:
            does_collide, colliding_sprite = self.does_collide(self.all_sprites)
            if does_collide:
                self.__rotate('left')

    def move_left(self):
        self.rect.x -= self.tetromino_size
        does_collide, colliding_sprite = self.does_collide(self.all_sprites)
        if does_collide:
            self.rect.x += self.tetromino_size

    def move_right(self):
        self.rect.x += self.tetromino_size
        does_collide, colliding_sprite = self.does_collide(self.all_sprites)
        if does_collide:
            self.rect.x -= self.tetromino_size

    def move_down(self):
        self.rect.y += self.tetromino_size
        does_collide, colliding_sprite = self.does_collide(self.all_sprites)
        if does_collide:
            self.rect.y -= self.tetromino_size

    def move_down_force(self):
        self.rect.y += self.tetromino_size

    def is_bottom(self):
        if self.rect.y == self.playing_area_bottom - self.image.get_height():
            return True
        return False

    def does_collide(self, _sprite_group):
        for t in _sprite_group:
            if t == self:
                continue
            if pg.sprite.collide_mask(self, t) is not None:
                return True, t
        return False, None

    def would_collide(self, _sprite_group):
        self.rect.y += self.tetromino_size
        does_collide, colliding_sprite = self.does_collide(_sprite_group)
        if does_collide:
            self.rect.y -= self.tetromino_size
            return True
        self.rect.y -= self.tetromino_size
        return False


class SingleBlock(Tetromino):
    def __init__(self, _screen, _playing_area_bottom, _playing_area_left,
                 _playing_area_right, _tetromino_size, _all_sprites, _color):
        super(SingleBlock, self).__init__(_screen, _playing_area_bottom, _playing_area_left,
                                          _playing_area_right, _tetromino_size, _all_sprites, _color)
        self.shapes = [
            [
                [1]
            ]
        ]
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.tetromino_size,
                                 len(self.shapes[self.current_shape]) * self.tetromino_size))
        self.rect = self.image.get_rect()
        self.draw()

    def rotate_left(self):
        pass

    def rotate_right(self):
        pass


class Straight(Tetromino):
    def __init__(self, _screen, _playing_area_bottom, _playing_area_left,
                 _playing_area_right, _tetromino_size, _all_sprites):
        super(Straight, self).__init__(_screen, _playing_area_bottom, _playing_area_left,
                                       _playing_area_right, _tetromino_size, _all_sprites, Colors.TetroStraight)
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
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.tetromino_size,
                                 len(self.shapes[self.current_shape]) * self.tetromino_size))
        self.rect = self.image.get_rect()
        self.draw()


class Square(Tetromino):
    def __init__(self, _screen, _playing_area_bottom, _playing_area_left,
                 _playing_area_right, _tetromino_size, _all_sprites):
        super(Square, self).__init__(_screen, _playing_area_bottom, _playing_area_left,
                                     _playing_area_right, _tetromino_size, _all_sprites, Colors.TetroSquare)
        self.shapes = [
            [
                [1, 1],
                [1, 1]
            ]
        ]
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.tetromino_size,
                                 len(self.shapes[self.current_shape]) * self.tetromino_size))
        self.rect = self.image.get_rect()
        self.draw()

    def rotate_left(self):
        pass

    def rotate_right(self):
        pass


class T(Tetromino):
    def __init__(self, _screen, _playing_area_bottom, _playing_area_left,
                 _playing_area_right, _tetromino_size, _all_sprites):
        super(T, self).__init__(_screen, _playing_area_bottom, _playing_area_left,
                                _playing_area_right, _tetromino_size, _all_sprites, Colors.TetroT)
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
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.tetromino_size,
                                 len(self.shapes[self.current_shape]) * self.tetromino_size))
        self.rect = self.image.get_rect()
        self.draw()


class L(Tetromino):
    def __init__(self, _screen, _playing_area_bottom, _playing_area_left,
                 _playing_area_right, _tetromino_size, _all_sprites):
        super(L, self).__init__(_screen, _playing_area_bottom, _playing_area_left,
                                _playing_area_right, _tetromino_size, _all_sprites, Colors.TetroL)
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
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.tetromino_size,
                                 len(self.shapes[self.current_shape]) * self.tetromino_size))
        self.rect = self.image.get_rect()
        self.draw()


class J(Tetromino):
    def __init__(self, _screen, _playing_area_bottom, _playing_area_left,
                 _playing_area_right, _tetromino_size, _all_sprites):
        super(J, self).__init__(_screen, _playing_area_bottom, _playing_area_left,
                                _playing_area_right, _tetromino_size, _all_sprites, Colors.TetroJ)
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
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.tetromino_size,
                                 len(self.shapes[self.current_shape]) * self.tetromino_size))
        self.rect = self.image.get_rect()
        self.draw()


class S(Tetromino):
    def __init__(self, _screen, _playing_area_bottom, _playing_area_left,
                 _playing_area_right, _tetromino_size, _all_sprites):
        super(S, self).__init__(_screen, _playing_area_bottom, _playing_area_left,
                                _playing_area_right, _tetromino_size, _all_sprites, Colors.TetroS)
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
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.tetromino_size,
                                 len(self.shapes[self.current_shape]) * self.tetromino_size))
        self.rect = self.image.get_rect()
        self.draw()


class Z(Tetromino):
    def __init__(self, _screen, _playing_area_bottom, _playing_area_left,
                 _playing_area_right, _tetromino_size, _all_sprites):
        super(Z, self).__init__(_screen, _playing_area_bottom, _playing_area_left,
                                _playing_area_right, _tetromino_size, _all_sprites, Colors.TetroZ)
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
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * self.tetromino_size,
                                 len(self.shapes[self.current_shape]) * self.tetromino_size))
        self.rect = self.image.get_rect()
        self.draw()
