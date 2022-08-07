# -*- coding: utf-8 -*-

import pygame as pg
from libs.constants import *
from libs.colors import *


class Tetromino(pg.sprite.Sprite):
    def __init__(self, _screen, _all_sprites, _color):
        super(Tetromino, self).__init__()
        self.shapes = [[[]]]
        self.shape_widths = []
        self.shape_heights = []
        self.current_shape = 0
        self.screen = _screen
        self.color = _color
        self.mask = None
        self.all_sprites = _all_sprites

    def draw(self):
        num_blocks_hori = len(self.shapes[self.current_shape][0])
        num_blocks_verti = len(self.shapes[self.current_shape])

        self.image = pg.Surface((num_blocks_hori * TETROMINO_SIZE,
                                 num_blocks_verti * TETROMINO_SIZE))

        for j in range(num_blocks_verti):
            for i in range(num_blocks_hori):
                if self.shapes[self.current_shape][j][i]:
                    pg.draw.polygon(surface=self.image, color=self.color.bg_topleft,
                                    points=[(0 + i * TETROMINO_SIZE, (TETROMINO_SIZE - 1) + j * TETROMINO_SIZE),
                                            (0 + i * TETROMINO_SIZE, 0 + j * TETROMINO_SIZE),
                                            ((TETROMINO_SIZE - 1) + i * TETROMINO_SIZE, 0 + j * TETROMINO_SIZE)])
                    pg.draw.polygon(surface=self.image, color=self.color.bg_bottomright,
                                    points=[(0 + i * TETROMINO_SIZE,
                                             (TETROMINO_SIZE - 1) + j * TETROMINO_SIZE),
                                            ((TETROMINO_SIZE - 1) + i * TETROMINO_SIZE,
                                             0 + j * TETROMINO_SIZE),
                                            ((TETROMINO_SIZE - 1) + i * TETROMINO_SIZE,
                                             (TETROMINO_SIZE - 1) + j * TETROMINO_SIZE)])
                    pg.draw.rect(self.image,
                                 color=self.color.fg_square,
                                 rect=(int(round(TETROMINO_SIZE / 8)) + i * TETROMINO_SIZE,
                                       int(round(TETROMINO_SIZE / 8)) + j * TETROMINO_SIZE,
                                       int(round(TETROMINO_SIZE / (4 / 3))),
                                       int(round(TETROMINO_SIZE / (4 / 3)))))

        self.image.set_colorkey(Colors.BLACK)
        self.mask = pg.mask.from_surface(self.image)

    def clear_single_block(self):
        self.image = pg.Surface((35, 35))
        pg.draw.rect(self.image,
                     color=Colors.TetroS.fg_square,
                     rect=(0,
                           0,
                           TETROMINO_SIZE,
                           TETROMINO_SIZE))

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

        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * TETROMINO_SIZE,
                                 len(self.shapes[self.current_shape]) * TETROMINO_SIZE))
        self.draw()

    def rotate_right(self):
        self.__rotate('right')
        if self.rect.y > PLAYING_AREA_BOTTOM - self.image.get_height() or \
                self.rect.x < PLAYING_AREA_LEFT or \
                self.rect.x > PLAYING_AREA_RIGHT - self.image.get_width():
            self.__rotate('left')
        else:
            does_collide, colliding_sprite = Tetromino.does_collide(self, self.all_sprites)
            if does_collide:
                self.__rotate('left')

    def move_left(self):
        self.rect.x -= TETROMINO_SIZE
        does_collide, colliding_sprite = Tetromino.does_collide(self, self.all_sprites)
        if does_collide:
            self.rect.x += TETROMINO_SIZE

    def move_right(self):
        self.rect.x += TETROMINO_SIZE
        does_collide, colliding_sprite = Tetromino.does_collide(self, self.all_sprites)
        if does_collide:
            self.rect.x -= TETROMINO_SIZE

    def move_down(self):
        self.rect.y += TETROMINO_SIZE
        does_collide, colliding_sprite = Tetromino.does_collide(self, self.all_sprites)
        if does_collide:
            self.rect.y -= TETROMINO_SIZE

    def move_down_force(self):
        self.rect.y += TETROMINO_SIZE

    def is_bottom(self):
        if self.rect.y == PLAYING_AREA_BOTTOM - self.image.get_height():
            return True
        return False

    @staticmethod
    def does_collide(_tetromino, _sprite_group):
        for t in _sprite_group:
            if t == _tetromino:
                continue
            if pg.sprite.collide_mask(_tetromino, t) is not None:
                return True, t
        return False, None

    @staticmethod
    def would_collide(_tetromino, _sprite_group):
        _tetromino.rect.y += TETROMINO_SIZE
        does_collide, colliding_sprite = Tetromino.does_collide(_tetromino, _sprite_group)
        if does_collide:
            _tetromino.rect.y -= TETROMINO_SIZE
            return True
        _tetromino.rect.y -= TETROMINO_SIZE
        return False


class SingleBlock(Tetromino):
    def __init__(self, _screen, _all_sprites, _color):
        super(SingleBlock, self).__init__(_screen, _all_sprites, _color)
        self.shapes = [
            [
                [1]
            ]
        ]
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * TETROMINO_SIZE,
                                 len(self.shapes[self.current_shape]) * TETROMINO_SIZE))
        self.rect = self.image.get_rect()
        self.draw()

    def rotate_left(self):
        pass

    def rotate_right(self):
        pass


class Straight(Tetromino):
    def __init__(self, _screen, _all_sprites):
        super(Straight, self).__init__(_screen, _all_sprites, Colors.TetroStraight())
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
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * TETROMINO_SIZE,
                                 len(self.shapes[self.current_shape]) * TETROMINO_SIZE))
        self.rect = self.image.get_rect()
        self.draw()


class Square(Tetromino):
    def __init__(self, _screen, _all_sprites):
        super(Square, self).__init__(_screen, _all_sprites, Colors.TetroSquare())
        self.shapes = [
            [
                [1, 1],
                [1, 1]
            ]
        ]
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * TETROMINO_SIZE,
                                 len(self.shapes[self.current_shape]) * TETROMINO_SIZE))
        self.rect = self.image.get_rect()
        self.draw()

    def rotate_left(self):
        pass

    def rotate_right(self):
        pass


class T(Tetromino):
    def __init__(self, _screen, _all_sprites):
        super(T, self).__init__(_screen, _all_sprites, Colors.TetroT())
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
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * TETROMINO_SIZE,
                                 len(self.shapes[self.current_shape]) * TETROMINO_SIZE))
        self.rect = self.image.get_rect()
        self.draw()


class L(Tetromino):
    def __init__(self, _screen, _all_sprites):
        super(L, self).__init__(_screen, _all_sprites, Colors.TetroL())
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
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * TETROMINO_SIZE,
                                 len(self.shapes[self.current_shape]) * TETROMINO_SIZE))
        self.rect = self.image.get_rect()
        self.draw()


class J(Tetromino):
    def __init__(self, _screen, _all_sprites):
        super(J, self).__init__(_screen, _all_sprites, Colors.TetroJ())
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
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * TETROMINO_SIZE,
                                 len(self.shapes[self.current_shape]) * TETROMINO_SIZE))
        self.rect = self.image.get_rect()
        self.draw()


class S(Tetromino):
    def __init__(self, _screen, _all_sprites):
        super(S, self).__init__(_screen, _all_sprites, Colors.TetroS())
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
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * TETROMINO_SIZE,
                                 len(self.shapes[self.current_shape]) * TETROMINO_SIZE))
        self.rect = self.image.get_rect()
        self.draw()


class Z(Tetromino):
    def __init__(self, _screen, _all_sprites):
        super(Z, self).__init__(_screen, _all_sprites, Colors.TetroZ())
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
        self.image = pg.Surface((len(self.shapes[self.current_shape][0]) * TETROMINO_SIZE,
                                 len(self.shapes[self.current_shape]) * TETROMINO_SIZE))
        self.rect = self.image.get_rect()
        self.draw()
