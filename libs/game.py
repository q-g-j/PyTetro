# -*- coding: utf-8 -*-

import uuid
import random

from libs.fonts import *
from libs.frame import *
from libs.tetrominos import *


class Game:
    def __init__(self, _window, _constants, _all_sprites, _level, _sidebar):
        self.__window = _window
        self.__constants = _constants
        self.__all_sprites = _all_sprites
        self.__level = _level
        self.__sidebar = _sidebar

        self.__random = random.Random()
        self.__random.seed(uuid.uuid4().int)
        self.__clock = pg.time.Clock()
        self.__fonts = Fonts(self.__constants)
        self.__all_sprites_list = list()

        self.__initial_level = _level
        self.__points = 0

    def start(self):
        return self.__game_loop()

    def __game_loop(self):
        is_key_up_pressed = False
        current_tetromino = None
        self.__fps = 60
        pg.key.set_repeat(200, 50)
        game_over_tetromino_nums = [x for x in range(1, 8)]

        next_tetromino_num = self.__random.randint(1, 7)

        counter_move_down = 0
        counter_at_bottom = 0
        counter_drop = 0
        counter_has_lost = 0
        counter_print_game_over = 0

        is_running = True
        while is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    is_running = False
                if is_running \
                        and current_tetromino is not None \
                        and counter_has_lost == 0 \
                        and counter_print_game_over == 0:
                    if event.type == pg.KEYUP:
                        is_key_up_pressed = False
                    elif event.type == pg.KEYDOWN:
                        pressed_keys = pg.key.get_pressed()
                        if pressed_keys[pg.K_LEFT] and not pressed_keys[pg.K_RIGHT]:
                            pg.key.set_repeat(200, 50)
                            current_tetromino.move_left()
                            counter_at_bottom = 0
                        elif pressed_keys[pg.K_RIGHT] and not pressed_keys[pg.K_LEFT]:
                            pg.key.set_repeat(200, 50)
                            current_tetromino.move_right()
                            counter_at_bottom = 0
                        elif pressed_keys[pg.K_UP] and not is_key_up_pressed:
                            is_key_up_pressed = True
                            current_tetromino.rotate_right()
                            counter_at_bottom = 0
                        elif pressed_keys[pg.K_DOWN]:
                            does_collide, tetromino = current_tetromino.does_collide(self.__all_sprites)
                            if not does_collide:
                                pg.key.set_repeat(200, 30)
                                current_tetromino.move_down()

            if is_running \
                    and counter_print_game_over == 0 \
                    and counter_at_bottom == 0 \
                    and counter_drop == 0:
                if current_tetromino is None:
                    if counter_has_lost != 0:
                        tetromino_num_index = int(counter_has_lost / int(round(self.__fps / 2)))
                        tetromino_num = game_over_tetromino_nums[tetromino_num_index - 1]
                    else:
                        tetromino_num = next_tetromino_num
                        # tetromino_num = 1
                    current_tetromino = self.__create_tetromino(tetromino_num)
                    next_tetromino_num = self.__random.randint(1, 7)
                    if counter_has_lost == 0:
                        does_collide, colliding_tetromino = current_tetromino.does_collide(self.__all_sprites)
                        if does_collide:
                            counter_has_lost = 1
                elif current_tetromino.would_collide(self.__all_sprites) and counter_has_lost == 0:
                    counter_at_bottom = 1

                counter_move_down += 1

            if is_running \
                    and counter_has_lost != 0:
                counter_has_lost += 1
                if counter_has_lost % int(round(self.__fps / 2)) == 0:
                    current_tetromino = None
                if counter_has_lost == int(round(self.__fps / 2)) * 8:
                    counter_has_lost = 0
                    for tetromino in self.__all_sprites:
                        if type(tetromino) != FrameBlock:
                            tetromino.kill()
                    counter_print_game_over = 1
                    self.__print_game_over()

            if is_running \
                    and counter_print_game_over != 0:
                counter_print_game_over += 1
                if counter_print_game_over == int(round(self.__fps / 2)) * 8:
                    return True

            if is_running \
                    and counter_move_down != 0:
                if counter_has_lost == 0 \
                        and counter_print_game_over == 0 \
                        and counter_move_down % int(round(self.__fps / self.__level / 1.5)) == 0:
                    current_tetromino.move_down()
                    counter_move_down = 0

            if is_running \
                    and counter_at_bottom != 0:
                counter_at_bottom += 1
                if counter_at_bottom == int(round(self.__fps / 3)):
                    if current_tetromino.would_collide(self.__all_sprites):
                        self.__change_tetromino_to_single_blocks(current_tetromino, self.__all_sprites)
                        if self.__remove_full_rows(self.__all_sprites):
                            counter_drop = 1
                        current_tetromino = None
                        counter_at_bottom = 0
                        counter_move_down = 0

            if is_running \
                    and counter_drop != 0:
                counter_drop += 1
                if counter_drop == int(round(self.__fps / 3)):
                    counter_drop = 0

            if is_running \
                    and counter_print_game_over == 0:
                self.__window.fill(colors.Constants.SCREEN)
                self.__all_sprites.draw(self.__window)
                self.__sidebar.set_level(self.__level)
                self.__sidebar.set_points(self.__points)
                if counter_has_lost == 0:
                    self.__sidebar.set_next_tetromino(next_tetromino_num)
                else:
                    self.__sidebar.set_next_tetromino(0)
                self.__sidebar.draw()
                pg.display.update()

            if is_running:
                self.__clock.tick(self.__fps)

            if not is_running:
                return False

    def __create_tetromino(self, _number):
        current_tetromino = None
        if _number == 1:
            current_tetromino = Straight(self.__window, self.__constants, self.__all_sprites)
        elif _number == 2:
            current_tetromino = Square(self.__window, self.__constants, self.__all_sprites)
        elif _number == 3:
            current_tetromino = T(self.__window, self.__constants, self.__all_sprites)
        elif _number == 4:
            current_tetromino = L(self.__window, self.__constants, self.__all_sprites)
        elif _number == 5:
            current_tetromino = J(self.__window, self.__constants, self.__all_sprites)
        elif _number == 6:
            current_tetromino = S(self.__window, self.__constants, self.__all_sprites)
        elif _number == 7:
            current_tetromino = Z(self.__window, self.__constants, self.__all_sprites)

        current_tetromino.rect.x = \
            int(self.__constants.window_width / 2) - \
            int((current_tetromino.image.get_width() / self.__constants.block_size) / 2) * \
            self.__constants.block_size
        current_tetromino.rect.y = self.__constants.playing_area_top
        self.__all_sprites.add(current_tetromino)

        return current_tetromino

    def __change_tetromino_to_single_blocks(self, _tetromino: Tetromino, _all_sprites):
        color = colors.Constants.SCREEN
        if type(_tetromino) == Straight:
            color = colors.Tetrominos.Straight
        elif type(_tetromino) == Square:
            color = colors.Tetrominos.Square
        elif type(_tetromino) == T:
            color = colors.Tetrominos.T
        elif type(_tetromino) == L:
            color = colors.Tetrominos.L
        elif type(_tetromino) == J:
            color = colors.Tetrominos.J
        elif type(_tetromino) == S:
            color = colors.Tetrominos.S
        elif type(_tetromino) == Z:
            color = colors.Tetrominos.Z

        for x in range(
                _tetromino.rect.x, _tetromino.rect.x + _tetromino.image.get_width(), self.__constants.block_size):
            for y in range(
                    _tetromino.rect.y, _tetromino.rect.y + _tetromino.image.get_height(), self.__constants.block_size):
                rect = pg.rect.Rect((x, y, self.__constants.block_size, self.__constants.block_size))
                sprite = SingleBlock(self.__window, self.__constants, self.__all_sprites, color)
                sprite.rect = rect
                does_collide, colliding_sprite = sprite.does_collide(_all_sprites)
                if does_collide and type(colliding_sprite) != FrameBlock and type(colliding_sprite) != SingleBlock:
                    _all_sprites.add(sprite)
        _tetromino.kill()

        self.__window.fill(colors.Constants.SCREEN)
        _all_sprites.draw(self.__window)

    def __remove_full_rows(self, _all_sprites):
        has_removed = False
        count_removed_rows = 0

        for row in range(1, int(self.__constants.playing_area_bottom / self.__constants.block_size) + 1):
            row_blocks_rect_list = []
            for col in range(1, int(self.__constants.playing_area_right / self.__constants.block_size)):
                rect = pg.rect.Rect((col * self.__constants.block_size, row * self.__constants.block_size,
                                     self.__constants.block_size, self.__constants.block_size))
                sprite = SingleBlock(self.__window, self.__constants, self.__all_sprites, colors.Tetrominos.Square)
                sprite.rect = rect
                does_collide, colliding_sprite = Tetromino.does_collide(sprite, _all_sprites)
                if does_collide:
                    row_blocks_rect_list.append(colliding_sprite)

            if len(row_blocks_rect_list) == 12:
                count_removed_rows += 1
                has_removed = True
                for colliding_sprite in row_blocks_rect_list:
                    colliding_sprite.kill()
                self.__drop_after_remove(_all_sprites, row * self.__constants.block_size)

        self.__window.fill(colors.Constants.SCREEN)
        _all_sprites.draw(self.__window)

        # if count_removed_rows == 1:
        self.__points += int(((count_removed_rows ** 2) * 10) / 10) * 10

        actual_points = self.__points + self.__initial_level * 500 - 500

        if 500 <= actual_points < 1000:
            self.__level = 2
        elif 1000 <= actual_points < 1500:
            self.__level = 3
        elif 1500 <= actual_points < 2000:
            self.__level = 4
        elif 2000 <= actual_points < 2500:
            self.__level = 5
        elif 2500 <= actual_points < 3000:
            self.__level = 6
        elif 3000 <= actual_points < 3500:
            self.__level = 7
        elif 3500 <= actual_points < 4000:
            self.__level = 8
        elif 4000 <= actual_points < 4500:
            self.__level = 9
        elif 4500 <= actual_points < 5000:
            self.__level = 10

        return has_removed

    @staticmethod
    def __drop_after_remove(_all_sprites, _row):
        for tetromino in _all_sprites:
            if type(tetromino) != FrameBlock:
                if tetromino.rect.y < _row:
                    tetromino.move_down_force()

    def __print_game_over(self):
        text_surface = self.__fonts.game_over.render("Game Over", True, colors.Constants.RED)
        width = text_surface.get_width()
        height = text_surface.get_height()
        x = int(round(self.__constants.window_width / 2)) - int(round(width / 2))
        y = int(round(self.__constants.window_height / 3)) - int(round(height / 2))
        self.__window.fill(colors.Constants.SCREEN)
        self.__all_sprites.draw(self.__window)
        self.__window.blit(text_surface, (x, y))
        self.__sidebar.set_level(self.__level)
        self.__sidebar.set_points(self.__points)
        self.__sidebar.set_next_tetromino(0)
        self.__sidebar.draw()
        pg.display.update()
        pg.display.update()
