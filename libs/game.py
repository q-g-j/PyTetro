# -*- coding: utf-8 -*-

import uuid
import random

from libs.frame import *
from libs.sidebar import *
from libs.tetrominoes import *


class Game:
    def __init__(self, _window: pg.Surface, _sidebar: SideBar, _constants: Constants, _all_sprites: pg.sprite.Group,
                 _level: int):
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

        self.__removed_rows_per_level = 0
        self.__removed_rows_total = 0
        self.__points = 0

    def start(self) -> bool:
        return self.__game_loop()

    def __game_loop(self) -> bool:
        current_tetromino = None
        pg.key.set_repeat(200, 50)
        game_over_tetromino_counter = 0
        game_over_tetrominoes = [x for x in range(1, 8)]
        next_tetromino_num = self.__random.randint(1, 7)

        is_rotate_key_pressed = False
        is_game_paused = False

        has_lost = False
        do_print_game_over = False
        do_move_down_tetromino = False
        is_tetromino_at_bottom = False
        do_drop_tetrominoes = False

        delay_has_lost = 500 - int(round((self.__level - 1) * 15))
        delay_print_game_over = 5000
        delay_tetromino_move_down = 500 - int(round((self.__level - 1) * 24))
        delay_tetromino_at_bottom = 500 - int(round((self.__level - 1) * 15))
        delay_drop_tetrominoes = 500 - int(round((self.__level - 1) * 15))

        start_tetromino_move_down = 0
        start_tetromino_at_bottom = 0
        start_drop_tetrominoes = 0
        start_has_lost = 0
        start_print_game_over = 0

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
                        elif has_lost == 0 \
                                and not is_game_paused \
                                and not do_print_game_over \
                                and current_tetromino is not None:
                            if pressed_keys[pg.K_LEFT] or pressed_keys[pg.K_j]:
                                if not current_tetromino.would_collide_left(self.__all_sprites):
                                    pg.key.set_repeat(200, 50)
                                    current_tetromino.move_left()
                                    if not current_tetromino.would_collide_down(self.__all_sprites):
                                        is_tetromino_at_bottom = False
                            elif pressed_keys[pg.K_RIGHT] or pressed_keys[pg.K_l]:
                                if not current_tetromino.would_collide_right(self.__all_sprites):
                                    pg.key.set_repeat(200, 50)
                                    current_tetromino.move_right()
                                    if not current_tetromino.would_collide_down(self.__all_sprites):
                                        is_tetromino_at_bottom = False
                            if not is_rotate_key_pressed:
                                if (pressed_keys[pg.K_DOWN] or pressed_keys[pg.K_k]) and not pressed_keys[pg.K_SPACE]:
                                    is_rotate_key_pressed = True
                                    current_tetromino.rotate_left()
                                    if not current_tetromino.would_collide_down(self.__all_sprites):
                                        is_tetromino_at_bottom = False
                                elif (pressed_keys[pg.K_UP] or pressed_keys[pg.K_i]) and not pressed_keys[pg.K_SPACE]:
                                    is_rotate_key_pressed = True
                                    current_tetromino.rotate_right()
                                    if not current_tetromino.would_collide_down(self.__all_sprites):
                                        is_tetromino_at_bottom = False
                            if pressed_keys[pg.K_SPACE]:
                                if not current_tetromino.would_collide_down(self.__all_sprites):
                                    pg.key.set_repeat(150, 25)
                                    current_tetromino.move_down()

            if is_running:
                self.__window.fill(colors.Constants.SCREEN)

            if not is_game_paused:
                if is_running \
                        and not do_print_game_over \
                        and not do_drop_tetrominoes:
                    if current_tetromino is None:
                        if has_lost:
                            tetromino_num = game_over_tetrominoes[game_over_tetromino_counter - 1]
                        else:
                            tetromino_num = next_tetromino_num
                            # tetromino_num = 1
                        current_tetromino = self.__create_tetromino(tetromino_num)
                        next_tetromino_num = self.__random.randint(1, 7)
                        if not has_lost:
                            does_collide, colliding_tetromino = current_tetromino.does_collide(self.__all_sprites)
                            if does_collide:
                                has_lost = True
                                start_has_lost = pg.time.get_ticks()
                    elif current_tetromino.would_collide_down(self.__all_sprites) \
                            and not has_lost \
                            and not is_tetromino_at_bottom:
                        is_tetromino_at_bottom = True
                        start_tetromino_at_bottom = pg.time.get_ticks()

                    if not do_move_down_tetromino:
                        do_move_down_tetromino = True
                        start_tetromino_move_down = pg.time.get_ticks()

                if is_running \
                        and has_lost:
                    if pg.time.get_ticks() - start_has_lost > delay_has_lost:
                        if type(current_tetromino) == Straight:
                            game_over_tetrominoes[0] = 3
                            game_over_tetrominoes[2] = 1
                        current_tetromino = None
                        start_has_lost = pg.time.get_ticks()
                        game_over_tetromino_counter += 1
                    if game_over_tetromino_counter == 8:
                        for tetromino in self.__all_sprites:
                            if type(tetromino) != FrameBlock:
                                tetromino.kill()
                        do_print_game_over = True
                        start_print_game_over = pg.time.get_ticks()
                        has_lost = False

                if is_running \
                        and do_print_game_over:
                    self.__print_game_over()
                    if pg.time.get_ticks() - start_print_game_over > delay_print_game_over:
                        return True

                if is_running \
                        and do_move_down_tetromino \
                        and not has_lost \
                        and not do_print_game_over \
                        and pg.time.get_ticks() - start_tetromino_move_down > delay_tetromino_move_down:
                    if not current_tetromino.would_collide_down(self.__all_sprites):
                        current_tetromino.move_down()
                    do_move_down_tetromino = False

                if is_running \
                        and is_tetromino_at_bottom:
                    if pg.time.get_ticks() - start_tetromino_at_bottom > delay_tetromino_at_bottom:
                        if current_tetromino.would_collide_down(self.__all_sprites):
                            self.__change_tetromino_to_single_blocks(current_tetromino, self.__all_sprites)
                            if self.__remove_full_rows(self.__all_sprites):
                                do_drop_tetrominoes = True
                                start_drop_tetrominoes = pg.time.get_ticks()

                            current_tetromino = None
                            is_tetromino_at_bottom = False
                            do_move_down_tetromino = False

                if is_running \
                        and do_drop_tetrominoes:
                    if pg.time.get_ticks() - start_drop_tetrominoes > delay_drop_tetrominoes:
                        do_drop_tetrominoes = False

            if is_running \
                    and not do_print_game_over:
                self.__sidebar.set_level(self.__level)
                self.__sidebar.set_points(self.__points)
                if not has_lost:
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

    def __create_tetromino(self, _number: int) -> Tetromino:
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

    def __change_tetromino_to_single_blocks(self, _tetromino: Tetromino, _all_sprites: pg.sprite.Group):
        color = colors.Constants.SCREEN
        if type(_tetromino) == Straight:
            color = colors.TetrominoStraight
        elif type(_tetromino) == Square:
            color = colors.TetrominoSquare
        elif type(_tetromino) == T:
            color = colors.TetrominoT
        elif type(_tetromino) == L:
            color = colors.TetrominoL
        elif type(_tetromino) == J:
            color = colors.TetrominoJ
        elif type(_tetromino) == S:
            color = colors.TetrominoS
        elif type(_tetromino) == Z:
            color = colors.TetrominoZ

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

    def __remove_full_rows(self, _all_sprites: pg.sprite.Group) -> bool:
        has_removed = False
        count_removed_rows = 0

        for row in range(1, int(self.__constants.playing_area_bottom / self.__constants.block_size) + 1):
            row_blocks_rect_list = []
            for col in range(1, int(self.__constants.playing_area_right / self.__constants.block_size)):
                rect = pg.rect.Rect((col * self.__constants.block_size, row * self.__constants.block_size,
                                     self.__constants.block_size, self.__constants.block_size))
                sprite = SingleBlock(self.__window, self.__constants, self.__all_sprites, colors.TetrominoSquare)
                sprite.rect = rect
                does_collide, colliding_sprite = Tetromino.does_collide(sprite, _all_sprites)
                if does_collide:
                    row_blocks_rect_list.append(colliding_sprite)

            if len(row_blocks_rect_list) == 12:
                count_removed_rows += 1
                for colliding_sprite in row_blocks_rect_list:
                    colliding_sprite.kill()
                self.__drop_after_remove([x for x in _all_sprites], row * self.__constants.block_size)

        if count_removed_rows != 0:
            has_removed = True
            self.__points += int(((count_removed_rows ** 2) * 10) / 10) * 10

            if self.__level < self.__constants.max_level:
                self.__removed_rows_per_level += count_removed_rows
                self.__removed_rows_total += count_removed_rows
                rows_needed = self.__level - 1 + self.__constants.min_rows_needed_for_level_up
                if self.__removed_rows_per_level >= rows_needed:
                    self.__removed_rows_per_level = self.__removed_rows_per_level - rows_needed
                    self.__level += 1

        return has_removed

    @staticmethod
    def __drop_after_remove(_all_sprites_list: list, _row: int):
        for tetromino in _all_sprites_list:
            if type(tetromino) != FrameBlock:
                if tetromino.rect.y < _row:
                    tetromino.move_down()

    def __print_game_over(self):
        text_surface = self.__fonts.game_over.render("game over", True, colors.Constants.RED)
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
