# -*- coding: utf-8 -*-

import uuid
import random

from libs.fonts import *
from libs.frame import *
from libs.tetrominoes import *


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
        is_rotate_key_pressed = False
        current_tetromino = None
        pg.key.set_repeat(200, 50)
        game_over_tetromino_nums = [x for x in range(1, 8)]
        next_tetromino_num = self.__random.randint(1, 7)

        is_game_paused = False
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
                if is_running:
                    if event.type == pg.KEYUP:
                        is_rotate_key_pressed = False
                    elif event.type == pg.KEYDOWN:
                        pressed_keys = pg.key.get_pressed()
                        if pressed_keys[pg.K_PAUSE] or pressed_keys[pg.K_p]:
                            is_game_paused = not is_game_paused
                        elif pressed_keys[pg.K_LEFT] or pressed_keys[pg.K_j]:
                            if counter_has_lost == 0 \
                                    and not is_game_paused \
                                    and counter_print_game_over == 0 \
                                    and current_tetromino is not None:
                                if not current_tetromino.would_collide_left(self.__all_sprites):
                                    pg.key.set_repeat(200, 50)
                                    current_tetromino.move_left()
                        elif pressed_keys[pg.K_RIGHT] or pressed_keys[pg.K_l]:
                            if counter_has_lost == 0 \
                                    and not is_game_paused \
                                    and counter_print_game_over == 0 \
                                    and current_tetromino is not None:
                                if not current_tetromino.would_collide_right(self.__all_sprites):
                                    pg.key.set_repeat(200, 50)
                                    current_tetromino.move_right()
                        if (pressed_keys[pg.K_DOWN] or pressed_keys[pg.K_k]) and not pressed_keys[pg.K_SPACE]:
                            if not is_rotate_key_pressed \
                                    and counter_has_lost == 0 \
                                    and not is_game_paused \
                                    and counter_print_game_over == 0 \
                                    and current_tetromino is not None:
                                is_rotate_key_pressed = True
                                current_tetromino.rotate_left()
                        elif (pressed_keys[pg.K_UP] or pressed_keys[pg.K_i]) and not pressed_keys[pg.K_SPACE]:
                            if not is_rotate_key_pressed \
                                    and counter_has_lost == 0 \
                                    and not is_game_paused \
                                    and counter_print_game_over == 0 \
                                    and current_tetromino is not None:
                                is_rotate_key_pressed = True
                                current_tetromino.rotate_right()
                        if pressed_keys[pg.K_SPACE]:
                            if counter_has_lost == 0 \
                                    and not is_game_paused \
                                    and counter_print_game_over == 0 \
                                    and current_tetromino is not None:
                                if not current_tetromino.would_collide_down(self.__all_sprites):
                                    pg.key.set_repeat(200, 30)
                                    current_tetromino.move_down()

            if is_running:
                self.__window.fill(colors.Constants.SCREEN)

            if is_running \
                    and not is_game_paused \
                    and counter_print_game_over == 0 \
                    and counter_at_bottom == 0 \
                    and counter_drop == 0:
                if current_tetromino is None:
                    if counter_has_lost != 0:
                        tetromino_num_index = int(counter_has_lost / int(round(self.__constants.fps / 2)))
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
                elif current_tetromino.would_collide_down(self.__all_sprites) and counter_has_lost == 0:
                    counter_at_bottom = 1

                counter_move_down += 1

            if is_running \
                    and not is_game_paused \
                    and counter_has_lost != 0:
                counter_has_lost += 1
                if counter_has_lost % int(round(self.__constants.fps / 2)) == 0:
                    current_tetromino = None
                if counter_has_lost == int(round(self.__constants.fps / 2)) * 8:
                    for tetromino in self.__all_sprites:
                        if type(tetromino) != FrameBlock:
                            tetromino.kill()
                    counter_print_game_over = 1
                    counter_has_lost = 0

            if is_running \
                    and not is_game_paused \
                    and counter_print_game_over != 0:
                counter_print_game_over += 1
                self.__print_game_over()
                if counter_print_game_over == int(round(self.__constants.fps / 2)) * 8:
                    return True

            if is_running \
                    and not is_game_paused \
                    and counter_move_down != 0:
                if counter_has_lost == 0 \
                        and counter_print_game_over == 0 \
                        and counter_move_down % int(round(self.__constants.fps / (self.__level + 1) / 0.5)) == 0:
                    if not current_tetromino.would_collide_down(self.__all_sprites):
                        current_tetromino.move_down()
                    else:
                        counter_move_down = 0

            if is_running \
                    and not is_game_paused \
                    and counter_at_bottom != 0:
                counter_at_bottom += 1
                if counter_at_bottom == int(round(self.__constants.fps / 3)):
                    if current_tetromino.would_collide_down(self.__all_sprites):
                        self.__change_tetromino_to_single_blocks(current_tetromino, self.__all_sprites)
                        if self.__remove_full_rows(self.__all_sprites):
                            counter_drop = 1
                        current_tetromino = None
                        counter_at_bottom = 0
                        counter_move_down = 0

            if is_running \
                    and not is_game_paused \
                    and counter_drop != 0:
                counter_drop += 1
                if counter_drop == int(round(self.__constants.fps / 3)):
                    counter_drop = 0

            if is_running \
                    and counter_print_game_over == 0:
                self.__sidebar.set_level(self.__level)
                self.__sidebar.set_points(self.__points)
                if counter_has_lost == 0:
                    self.__sidebar.set_next_tetromino(next_tetromino_num)
                else:
                    self.__sidebar.set_next_tetromino(0)

            if is_running:
                self.__sidebar.draw()
                self.__all_sprites.draw(self.__window)
                if is_game_paused:
                    self.__pause_game()
                pg.display.update()
                self.__clock.tick(self.__constants.fps)

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
            color = colors.Tetrominoes.Straight
        elif type(_tetromino) == Square:
            color = colors.Tetrominoes.Square
        elif type(_tetromino) == T:
            color = colors.Tetrominoes.T
        elif type(_tetromino) == L:
            color = colors.Tetrominoes.L
        elif type(_tetromino) == J:
            color = colors.Tetrominoes.J
        elif type(_tetromino) == S:
            color = colors.Tetrominoes.S
        elif type(_tetromino) == Z:
            color = colors.Tetrominoes.Z

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

    def __remove_full_rows(self, _all_sprites):
        has_removed = False
        count_removed_rows = 0

        for row in range(1, int(self.__constants.playing_area_bottom / self.__constants.block_size) + 1):
            row_blocks_rect_list = []
            for col in range(1, int(self.__constants.playing_area_right / self.__constants.block_size)):
                rect = pg.rect.Rect((col * self.__constants.block_size, row * self.__constants.block_size,
                                     self.__constants.block_size, self.__constants.block_size))
                sprite = SingleBlock(self.__window, self.__constants, self.__all_sprites, colors.Tetrominoes.Square)
                sprite.rect = rect
                does_collide, colliding_sprite = Tetromino.does_collide(sprite, _all_sprites)
                if does_collide:
                    row_blocks_rect_list.append(colliding_sprite)

            if len(row_blocks_rect_list) == 12:
                count_removed_rows += 1
                for colliding_sprite in row_blocks_rect_list:
                    colliding_sprite.kill()
                self.__drop_after_remove(_all_sprites, row * self.__constants.block_size)

        if count_removed_rows != 0:
            has_removed = True
            self.__points += int(((count_removed_rows ** 2) * 10) / 10) * 10

        if self.__level < self.__constants.max_level:
            if self.__points >= self.__level * 500:
                self.__level += 1

        return has_removed

    @staticmethod
    def __drop_after_remove(_all_sprites, _row):
        for tetromino in _all_sprites:
            if type(tetromino) != FrameBlock:
                if tetromino.rect.y < _row:
                    tetromino.move_down()

    def __print_game_over(self):
        text_surface = self.__fonts.game_over.render("Game Over", True, colors.Constants.RED)
        width = text_surface.get_width()
        height = text_surface.get_height()
        x = int(round(self.__constants.window_width / 2)) - int(round(width / 2))
        y = int(round(self.__constants.window_height / 3)) - int(round(height / 2))
        self.__sidebar.set_level(self.__level)
        self.__sidebar.set_points(self.__points)
        self.__sidebar.set_next_tetromino(0)
        self.__window.blit(text_surface, (x, y))

    def __pause_game(self):
        text_surface = self.__fonts.game_over.render("Game paused", True, colors.Constants.RED)
        width = text_surface.get_width()
        height = text_surface.get_height()
        x = int(round(self.__constants.window_width / 2)) - int(round(width / 2))
        y = int(round(self.__constants.window_height / 3)) - int(round(height / 2))
        self.__sidebar.set_level(self.__level)
        self.__sidebar.set_points(self.__points)
        self.__sidebar.set_next_tetromino(0)
        self.__window.blit(text_surface, (x, y))
