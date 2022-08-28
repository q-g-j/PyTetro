# -*- coding: utf-8 -*-

import uuid
import random

from libs.frame import *
from libs.sidebar import *
from libs.tetrominoes import *


class Game:
    def __init__(self, _window: pg.Surface, _sidebar: SideBar, _constants: Constants, _all_sprites: pg.sprite.Group,
                 _level: int):
        """
        The constructor of class Game
        :param _window: the main surface for the whole game
        :param _sidebar: the sidebar that is only visible during gameplay
        :param _constants: an object of type Constants holding values like sizes and delays
        :param _all_sprites: a pygame sprite group containing all sprites (frame blocks and tetrominos)
        :param _level: the starting level representing the difficulty
        """
        self.__window = _window
        self.__constants = _constants
        self.__all_sprites = _all_sprites
        self.__level = _level
        self.__sidebar = _sidebar

        self.__random = random.Random()
        self.__random.seed(uuid.uuid4().int)
        self.__clock = pg.time.Clock()
        self.__fonts = Fonts(self.__constants)

        self.__cleared_lines_per_level = 0
        self.__cleared_lines_total = 0
        self.__points = 0

        self.__delay_tetromino_move_down_fps = 0
        self.__delay_tetromino_at_bottom_fps = 0
        self.__delay_drop_tetrominoes_fps = 0
        self.__delay_has_lost_fps = 0
        self.__delay_print_game_over_fps = 0

        self.__calc_delays()

    def start(self) -> bool:
        """
        Start the main loop from outside

        :return: was the program closed? True|False
        """
        return self.__game_loop()

    def __game_loop(self) -> bool:
        """
        The main gameplay loop.
        "clock.tick(fps)" at the end of the loop ensures that the screen is not redrawn
        more frequently per second than specified in the fps constant.
        All delays used to simulate the game speed are fractions of the fps constant calculated in the method
        "self.__calc_delays()"

        :return: was the program closed? True|False
        """
        current_tetromino = None
        pg.key.set_repeat(200, 50)
        game_over_tetromino_counter = 0
        game_over_tetrominoes = [x for x in range(1, 8)]
        next_tetromino_num = self.__random.randint(1, 7)

        is_rotate_key_pressed = False
        is_game_paused = False

        do_move_down_tetromino = False
        is_tetromino_at_bottom = False
        do_drop_tetrominoes = False
        has_lost = False
        do_print_game_over = False

        counter_tetromino_move_down = 0
        counter_tetromino_at_bottom = 0
        counter_drop_tetrominoes = 0
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
                        elif not has_lost \
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
                            colliding_tetromino = current_tetromino.does_collide(self.__all_sprites)
                            if colliding_tetromino is not None:
                                has_lost = True
                                counter_has_lost = 0
                    elif current_tetromino.would_collide_down(self.__all_sprites) \
                            and not has_lost \
                            and not is_tetromino_at_bottom:
                        is_tetromino_at_bottom = True
                        counter_tetromino_at_bottom = 0

                    if not do_move_down_tetromino:
                        do_move_down_tetromino = True
                        counter_tetromino_move_down = 0

                if is_running \
                        and do_move_down_tetromino:
                    if counter_tetromino_move_down < self.__delay_tetromino_move_down_fps:
                        counter_tetromino_move_down += 1

                if is_running \
                        and is_tetromino_at_bottom:
                    if counter_tetromino_at_bottom < self.__delay_tetromino_at_bottom_fps:
                        counter_tetromino_at_bottom += 1

                if is_running \
                        and has_lost:
                    if counter_has_lost < self.__delay_has_lost_fps:
                        counter_has_lost += 1

                if is_running \
                        and do_print_game_over:
                    if counter_print_game_over < self.__delay_print_game_over_fps:
                        counter_print_game_over += 1

                if is_running \
                        and has_lost:
                    if counter_has_lost == self.__delay_has_lost_fps:
                        if type(current_tetromino) == Straight:
                            game_over_tetrominoes[0] = 3
                            game_over_tetrominoes[2] = 1
                        current_tetromino = None
                        counter_has_lost = 0
                        game_over_tetromino_counter += 1
                    if game_over_tetromino_counter == 8:
                        for tetromino in self.__all_sprites:
                            if type(tetromino) != FrameBlock:
                                tetromino.kill()
                        do_print_game_over = True
                        has_lost = False

                if is_running \
                        and do_print_game_over:
                    self.__print_game_over()
                    if counter_print_game_over == self.__delay_print_game_over_fps:
                        return True

                if is_running \
                        and do_move_down_tetromino \
                        and not has_lost \
                        and not do_print_game_over \
                        and counter_tetromino_move_down == self.__delay_tetromino_move_down_fps:
                    if not current_tetromino.would_collide_down(self.__all_sprites):
                        current_tetromino.move_down()
                    do_move_down_tetromino = False
                    counter_tetromino_move_down = 0

                if is_running \
                        and is_tetromino_at_bottom \
                        and counter_tetromino_at_bottom == self.__delay_tetromino_at_bottom_fps:
                    if current_tetromino.would_collide_down(self.__all_sprites):
                        self.__change_tetromino_to_single_blocks(current_tetromino)
                        if self.__remove_full_lines(self.__all_sprites):
                            do_drop_tetrominoes = True
                            counter_drop_tetrominoes = 0

                        current_tetromino = None
                        is_tetromino_at_bottom = False
                        do_move_down_tetromino = False

                if is_running \
                        and do_drop_tetrominoes:
                    if counter_drop_tetrominoes < self.__delay_drop_tetrominoes_fps:
                        counter_drop_tetrominoes += 1
                    else:
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
        """
        Create a new sprite (as a subclass of class Tetromino) to appear at the top of the window and
        add it to the sprite group "self.__all_sprites"
        :param _number: an integer from 1 to 7
        :return: a sprite (as a subclass of class Tetromino)
        """
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

    def __change_tetromino_to_single_blocks(self, _tetromino: Tetromino):
        """
        Takes a sprite (as a subclass of class Tetromino) as param and converts each visible block into a
        seperate sprite, adds the latter to the main sprite group ("self.__all_sprites") and deletes the
        original tetromino from the sprite group
        :param _tetromino: a sprite of type Tetromino
        """
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
                colliding_sprite = sprite.does_collide(self.__all_sprites)
                if colliding_sprite is not None and type(colliding_sprite) != FrameBlock \
                        and type(colliding_sprite) != SingleBlock:
                    self.__all_sprites.add(sprite)
        _tetromino.kill()

    def __remove_full_lines(self, _all_sprites: pg.sprite.Group) -> bool:
        """
        Remove all blocks from full lines visibly and from their sprite group
        :param _all_sprites: the sprite group containing all tetrominoes and frame blocks
        :return: was at least one line removed? True|False
        """
        has_removed = False
        count_cleared_lines = 0

        for line in range(1, int(self.__constants.playing_area_bottom / self.__constants.block_size) + 1):
            line_blocks_rect_list = []
            for col in range(1, int(self.__constants.playing_area_right / self.__constants.block_size)):
                rect = pg.rect.Rect((col * self.__constants.block_size, line * self.__constants.block_size,
                                     self.__constants.block_size, self.__constants.block_size))
                sprite = SingleBlock(self.__window, self.__constants, self.__all_sprites, colors.TetrominoSquare)
                sprite.rect = rect
                colliding_sprite = Tetromino.does_collide(sprite, _all_sprites)
                if colliding_sprite is not None:
                    line_blocks_rect_list.append(colliding_sprite)

            if len(line_blocks_rect_list) == 12:
                count_cleared_lines += 1
                for colliding_sprite in line_blocks_rect_list:
                    colliding_sprite.kill()
                self.__drop_after_remove([x for x in _all_sprites], line * self.__constants.block_size)

        if count_cleared_lines != 0:
            has_removed = True
            self.__points += int((count_cleared_lines ** 2) * 10)

            if self.__level < self.__constants.max_level:
                self.__cleared_lines_per_level += count_cleared_lines
                self.__cleared_lines_total += count_cleared_lines
                lines_needed = self.__level - 1 + self.__constants.lines_needed_for_first_level_up
                if self.__cleared_lines_per_level >= lines_needed:
                    self.__cleared_lines_per_level = self.__cleared_lines_per_level - lines_needed
                    self.__level += 1
                    self.__calc_delays()

        return has_removed

    @staticmethod
    def __drop_after_remove(_all_sprites_list: list, _line_num: int):
        """
        Drop down all lines above the cleared line(s).
        Takes a list of all sprites (not a sprite group!) and the topmost cleared line as an integer
        :param _all_sprites_list: the sprite group containing all tetrominoes and frame blocks
        :param _line_num: int
        """
        for tetromino in _all_sprites_list:
            if type(tetromino) != FrameBlock:
                if tetromino.rect.y < _line_num:
                    tetromino.move_down()

    def __print_game_over(self):
        """
        A simple "game over" message when the game is lost, positioned in the top third of the window.
        """
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
        """
        A simple "game paused" message, positioned in the top third of the window.
        """
        text_surface = self.__fonts.game_over.render("game paused", True, colors.Constants.RED)
        width = text_surface.get_width()
        height = text_surface.get_height()
        x = int(round(self.__constants.window_width / 2)) - int(round(width / 2))
        y = int(round(self.__constants.window_height / 3)) - int(round(height / 2))
        self.__sidebar.set_level(self.__level)
        self.__sidebar.set_points(self.__points)
        self.__sidebar.set_next_tetromino(0)
        self.__window.blit(text_surface, (x, y))

    def __calc_delays(self):
        """
        Calculate several delays used during the game, e.g. for the speed of the falling tetrominoes or the pause
        before a new tetromino appears.
        Must be run once at game start and again after each level up.
        Uses constants starting with 'level_diff_' from class Constants which hold integers representing
        the delays in ms and converts them into a fraction of the fps the game runs at.
        """
        self.__delay_tetromino_move_down_fps = int(round(
            self.__constants.fps * (500 - (self.__level - 1) *
                                    self.__constants.level_diff_tetromino_move_down_ms) / 1000))
        self.__delay_tetromino_at_bottom_fps = int(round(
            self.__constants.fps * (500 - (self.__level - 1) *
                                    self.__constants.level_diff_tetromino_at_bottom_ms) / 1000))
        self.__delay_drop_tetrominoes_fps = int(round(
            self.__constants.fps * (500 - (self.__level - 1) *
                                    self.__constants.level_diff_drop_tetrominoes_ms) / 1000))
        self.__delay_has_lost_fps = int(round(
            self.__constants.fps * (500 - (self.__level - 1) *
                                    self.__constants.level_diff_has_lost_ms) / 1000))
        self.__delay_print_game_over_fps = int(round(
            self.__constants.fps * (self.__constants.delay_print_game_over_ms / 1000)))
