# -*- coding: utf-8 -*-


from libs.fonts import *
from libs.tetrominoes import *


class SideBar:
    def __init__(self, _window, _constants: Constants):
        self.__window = _window
        self.__constants = _constants

        self.__fonts = Fonts(self.__constants)
        self.__level = 0
        self.__points = 0
        self.__next_tetromino_number = 0

    def draw(self):
        text_level_surface = self.__fonts.sidebar_level.render(
            "level: " + str(self.__level), True, colors.Constants.RED)
        text_level_surface_width = text_level_surface.get_width()
        text_level_surface_height = text_level_surface.get_height()
        text_level_surface_x = int(round(self.__constants.window_width + self.__constants.sidebar_width / 2)) \
            - int(round(text_level_surface_width / 2))
        text_level_surface_y = int(round(self.__constants.window_height / 10)) \
            - int(round(text_level_surface_height / 2))
        self.__window.blit(text_level_surface, (text_level_surface_x, text_level_surface_y))

        text_points_surface = self.__fonts.sidebar_points.render(
            "points: " + str(self.__points), True, colors.Constants.BLUE)
        text_points_surface_width = text_points_surface.get_width()
        text_points_surface_height = text_points_surface.get_height()
        text_points_surface_x = int(round(self.__constants.window_width + self.__constants.sidebar_width / 2)) \
            - int(round(text_points_surface_width / 2))
        text_points_surface_y = text_level_surface_y + text_points_surface_height * 3
        self.__window.blit(text_points_surface, (text_points_surface_x, text_points_surface_y))

        if self.__next_tetromino_number != 0:
            next_tetromino = self.__create_next_tetrommino(self.__next_tetromino_number)
            next_tetromino.draw()
            self.__window.blit(next_tetromino.image, next_tetromino.rect)

    def set_level(self, _level: int):
        self.__level = _level

    def set_points(self, _points: int):
        self.__points = _points

    def set_next_tetromino(self, _tetromino_number: int):
        self.__next_tetromino_number = _tetromino_number

    def __create_next_tetrommino(self, _number: int) -> Tetromino:
        next_tetromino = None
        if _number == 1:
            next_tetromino = Straight(self.__window, self.__constants, pg.sprite.Group())
        elif _number == 2:
            next_tetromino = Square(self.__window, self.__constants, pg.sprite.Group())
        elif _number == 3:
            next_tetromino = T(self.__window, self.__constants, pg.sprite.Group())
        elif _number == 4:
            next_tetromino = L(self.__window, self.__constants, pg.sprite.Group())
        elif _number == 5:
            next_tetromino = J(self.__window, self.__constants, pg.sprite.Group())
        elif _number == 6:
            next_tetromino = S(self.__window, self.__constants, pg.sprite.Group())
        elif _number == 7:
            next_tetromino = Z(self.__window, self.__constants, pg.sprite.Group())

        next_tetromino.rect.x = int(round(self.__constants.window_width + self.__constants.sidebar_width / 2)) \
            - int(round(next_tetromino.image.get_width() / 2))
        next_tetromino.rect.y = int(round(self.__constants.window_height / 2))
        return next_tetromino
