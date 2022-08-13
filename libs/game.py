# -*- coding: utf-8 -*-

import uuid
import random

from libs.fonts import *
from libs.frame import *
from libs.tetrominos import *


class Game:
    def __init__(self):
        pg.init()
        self.__random = random.Random()
        self.__random.seed(uuid.uuid4().int)
        self.__clock = pg.time.Clock()
        self.__fonts = Fonts()
        self.__block_size, self.__screen_width, self.__screen_height = self.__compute_sizes()
        self.__screen = pg.display.set_mode((self.__screen_width, self.__screen_height))
        self.__playing_area_top = 0
        self.__playing_area_left = self.__block_size
        self.__playing_area_right = self.__screen_width - self.__block_size
        self.__playing_area_bottom = self.__screen_height - self.__block_size
        self.__all_sprites = pg.sprite.Group()
        self.__all_sprites_list = list()

    def start(self):
        self.__create_frame()
        self.__main_loop()

    def __main_loop(self):
        is_key_up_pressed = False
        current_tetromino = None
        self.__fps = 60
        speed = 2
        pg.key.set_repeat(200, 50)
        game_over_tetromino_nums = [x for x in range(1, 8)]

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
                        elif pressed_keys[pg.K_RIGHT] and not pressed_keys[pg.K_LEFT]:
                            pg.key.set_repeat(200, 50)
                            current_tetromino.move_right()
                        elif pressed_keys[pg.K_UP] and not is_key_up_pressed:
                            is_key_up_pressed = True
                            current_tetromino.rotate_right()
                        elif pressed_keys[pg.K_DOWN]:
                            pg.key.set_repeat(200, 30)
                            current_tetromino.move_down()

            if is_running \
                    and counter_print_game_over == 0 \
                    and counter_at_bottom == 0:
                if current_tetromino is None:
                    if counter_has_lost != 0:
                        tetromino_num_index = int(counter_has_lost / int(round(self.__fps / 2)))
                        tetromino_num = game_over_tetromino_nums[tetromino_num_index - 1]
                    else:
                        tetromino_num = self.__random.randint(1, 7)
                        # tetromino_num = 1
                    current_tetromino = self.__create_tetromino(tetromino_num)
                    if counter_has_lost == 0:
                        does_collide, colliding_tetromino = current_tetromino.does_collide(self.__all_sprites)
                        if does_collide:
                            counter_has_lost = 1
                elif current_tetromino.would_collide(self.__all_sprites) and counter_has_lost == 0:
                    counter_at_bottom = 1

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
                    counter_print_game_over = 0

            if is_running \
                    and counter_has_lost == 0 \
                    and counter_print_game_over == 0:
                if counter_move_down != 0 and counter_move_down % int(round(self.__fps / (speed * 1.5))) == 0:
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

            if is_running \
                    and counter_drop != 0 \
                    and counter_drop < int(round(self.__fps / 4)):
                counter_drop += 1
            elif counter_drop == int(round(self.__fps / 4)):
                counter_drop = 0

            if is_running \
                    and counter_print_game_over == 0:
                self.__screen.fill(Colors.SCREEN)
                self.__all_sprites.draw(self.__screen)
                pg.display.update()
                counter_move_down += 1

            if is_running:
                self.__clock.tick(self.__fps)

            if not is_running:
                pg.quit()

    def __create_frame(self):
        for i in range(0, int(self.__playing_area_right / self.__block_size) + self.__block_size):
            frame_block = FrameBlock(self.__screen, self.__block_size)
            frame_block.rect.x = i * self.__block_size
            frame_block.rect.y = -self.__block_size
            self.__all_sprites.add(frame_block)
        for i in range(0, int(self.__playing_area_right / self.__block_size) + self.__block_size):
            frame_block = FrameBlock(self.__screen, self.__block_size)
            frame_block.rect.x = i * self.__block_size
            frame_block.rect.y = 21 * self.__block_size + self.__block_size
            self.__all_sprites.add(frame_block)
        for i in range(0, 22):
            frame_block = FrameBlock(self.__screen, self.__block_size)
            frame_block.rect.x = 0
            frame_block.rect.y = i * self.__block_size
            self.__all_sprites.add(frame_block)
        for i in range(0, 22):
            frame_block = FrameBlock(self.__screen, self.__block_size)
            frame_block.rect.x = int(self.__playing_area_right / self.__block_size) * self.__block_size
            frame_block.rect.y = i * self.__block_size
            self.__all_sprites.add(frame_block)

    def __create_tetromino(self, _number):
        current_tetromino = None
        if _number == 1:
            current_tetromino = Straight(self.__screen, self.__playing_area_bottom,
                                         self.__playing_area_left, self.__playing_area_right,
                                         self.__block_size, self.__all_sprites)
        elif _number == 2:
            current_tetromino = Square(self.__screen, self.__playing_area_bottom,
                                       self.__playing_area_left, self.__playing_area_right,
                                       self.__block_size, self.__all_sprites)
        elif _number == 3:
            current_tetromino = T(self.__screen, self.__playing_area_bottom,
                                  self.__playing_area_left, self.__playing_area_right,
                                  self.__block_size, self.__all_sprites)
        elif _number == 4:
            current_tetromino = L(self.__screen, self.__playing_area_bottom,
                                  self.__playing_area_left, self.__playing_area_right,
                                  self.__block_size, self.__all_sprites)
        elif _number == 5:
            current_tetromino = J(self.__screen, self.__playing_area_bottom,
                                  self.__playing_area_left, self.__playing_area_right,
                                  self.__block_size, self.__all_sprites)
        elif _number == 6:
            current_tetromino = S(self.__screen, self.__playing_area_bottom,
                                  self.__playing_area_left, self.__playing_area_right,
                                  self.__block_size, self.__all_sprites)
        elif _number == 7:
            current_tetromino = Z(self.__screen, self.__playing_area_bottom,
                                  self.__playing_area_left, self.__playing_area_right,
                                  self.__block_size, self.__all_sprites)

        current_tetromino.rect.x = \
            int(self.__screen_width / 2) - \
            int((current_tetromino.image.get_width() / self.__block_size) / 2) * \
            self.__block_size
        current_tetromino.rect.y = self.__playing_area_top
        self.__all_sprites.add(current_tetromino)

        return current_tetromino

    def __change_tetromino_to_single_blocks(self, _tetromino: Tetromino, _all_sprites):
        color = Colors.SCREEN
        if type(_tetromino) == Straight:
            color = Colors.TetroStraight
        elif type(_tetromino) == Square:
            color = Colors.TetroSquare
        elif type(_tetromino) == T:
            color = Colors.TetroT
        elif type(_tetromino) == L:
            color = Colors.TetroL
        elif type(_tetromino) == J:
            color = Colors.TetroJ
        elif type(_tetromino) == S:
            color = Colors.TetroS
        elif type(_tetromino) == Z:
            color = Colors.TetroZ

        for x in range(_tetromino.rect.x, _tetromino.rect.x + _tetromino.image.get_width(), self.__block_size):
            for y in range(_tetromino.rect.y, _tetromino.rect.y + _tetromino.image.get_height(), self.__block_size):
                rect = pg.rect.Rect((x, y, self.__block_size, self.__block_size))
                sprite = SingleBlock(self.__screen, self.__playing_area_bottom,
                                     self.__playing_area_left, self.__playing_area_right,
                                     self.__block_size, self.__all_sprites, color)
                sprite.rect = rect
                does_collide, colliding_sprite = sprite.does_collide(_all_sprites)
                if does_collide and type(colliding_sprite) != FrameBlock and type(colliding_sprite) != SingleBlock:
                    _all_sprites.add(sprite)
        _tetromino.kill()

        self.__screen.fill(Colors.SCREEN)
        _all_sprites.draw(self.__screen)

    def __remove_full_rows(self, _all_sprites):
        has_removed = False
        for row in range(1, int(self.__playing_area_bottom / self.__block_size) + 1):
            row_blocks_rect_list = []
            for col in range(1, int(self.__playing_area_right / self.__block_size)):
                rect = pg.rect.Rect((col * self.__block_size, row * self.__block_size,
                                     self.__block_size, self.__block_size))
                sprite = SingleBlock(self.__screen, self.__playing_area_bottom,
                                     self.__playing_area_left, self.__playing_area_right,
                                     self.__block_size, self.__all_sprites, Colors.TetroSquare)
                sprite.rect = rect
                does_collide, colliding_sprite = Tetromino.does_collide(sprite, _all_sprites)
                if does_collide:
                    row_blocks_rect_list.append(colliding_sprite)

            if len(row_blocks_rect_list) == 12:
                has_removed = True
                for colliding_sprite in row_blocks_rect_list:
                    colliding_sprite.kill()
                self.__drop_after_remove(_all_sprites, row * self.__block_size)

        self.__screen.fill(Colors.SCREEN)
        _all_sprites.draw(self.__screen)

        return has_removed

    @staticmethod
    def __drop_after_remove(_all_sprites, _row):
        for tetromino in _all_sprites:
            if type(tetromino) != FrameBlock:
                if tetromino.rect.y < _row:
                    tetromino.move_down_force()

    @staticmethod
    def __compute_sizes():
        screen_height = int(round(pg.display.Info().current_h * (2 / 3)))
        block_size = int(round(screen_height / 22))
        if block_size % 2 == 0:
            block_size += 1
        screen_width = block_size * 12 + 2 * block_size
        screen_height = block_size * 20 + 2 * block_size
        return block_size, screen_width, screen_height

    def __print_game_over(self):
        text_surface = self.__fonts.game_over.render("Game Over", True, Colors.RED)
        width = text_surface.get_width()
        height = text_surface.get_height()
        x = int(round(self.__screen_width / 2)) - int(round(width / 2))
        y = int(round(self.__screen_height / 3)) - int(round(height / 2))
        self.__screen.fill(Colors.SCREEN)
        self.__all_sprites.draw(self.__screen)
        self.__screen.blit(text_surface, (x, y))
        pg.display.update()
