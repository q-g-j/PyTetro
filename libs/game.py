# -*- coding: utf-8 -*-

import uuid
import random
from libs.frame import *
from libs.tetrominos import *


class Game:
    def __init__(self):
        pg.init()
        self.__random = random.Random()
        self.__random.seed(uuid.uuid4().int)
        self.__clock = pg.time.Clock()
        self.__tetromino_size, self.__screen_width, self.__screen_height = self.__compute_sizes()
        self.__screen = pg.display.set_mode((self.__screen_width, self.__screen_height))
        self.__playing_area_top = 0
        self.__playing_area_left = self.__tetromino_size
        self.__playing_area_right = self.__screen_width - self.__tetromino_size
        self.__playing_area_bottom = self.__screen_height - self.__tetromino_size
        self.__all_sprites = pg.sprite.Group()
        self.__all_sprites_list = list()

    def start(self):
        self.__create_frame()
        self.__main_loop()

    def __main_loop(self):
        is_key_up_pressed = False
        current_tetromino = None
        self.__fps = 60
        speed = 1
        pg.key.set_repeat(200, 50)

        counter = 0
        at_bottom_counter = 0
        game_over_tetromino_nums = [2, 5, 3, 1, 4, 7, 6]
        has_lost_counter = 0
        print_game_over_counter = 0
        self.__drop_counter = 0

        running = True
        while running:
            if print_game_over_counter == 0:
                if current_tetromino is None:
                    if has_lost_counter != 0:
                        tetromino_num_index = int(has_lost_counter / int(round(self.__fps / 2)))
                        tetromino_num = game_over_tetromino_nums[tetromino_num_index - 1]
                    else:
                        tetromino_num = self.__random.randint(1, 7)
                    current_tetromino = self.__create_tetromino(tetromino_num)
                    if has_lost_counter == 0:
                        does_collide, colliding_tetromino = current_tetromino.does_collide(self.__all_sprites)
                        if does_collide:
                            has_lost_counter = 1
                elif current_tetromino.would_collide(self.__all_sprites) and has_lost_counter == 0:
                    at_bottom_counter += 1

            if has_lost_counter != 0:
                has_lost_counter += 1
                if has_lost_counter % int(round(self.__fps / 2)) == 0:
                    current_tetromino = None
                if has_lost_counter == int(round(self.__fps / 2)) * 8:
                    has_lost_counter = 0
                    for tetromino in self.__all_sprites:
                        if type(tetromino) != FrameBlock:
                            tetromino.kill()
                    print_game_over_counter = 1
                    self.__screen.fill(Colors.SCREEN)
                    self.__all_sprites.draw(self.__screen)
                    self.__print_game_over()
                    pg.display.update()

            if print_game_over_counter != 0:
                print_game_over_counter += 1
                if print_game_over_counter == int(round(self.__fps / 2)) * 8:
                    print_game_over_counter = 0

            if has_lost_counter == 0 and print_game_over_counter == 0:
                if counter != 0 and counter % int(round(self.__fps / (speed * 2))) == 0:
                    current_tetromino.move_down()
                    counter = 0

                if at_bottom_counter == int(round(self.__fps / 2)):
                    at_bottom_counter = 0
                    self.__change_tetromino_to_single_blocks(current_tetromino, self.__all_sprites)
                    self.__remove_full_rows(self.__all_sprites)
                    current_tetromino = None
                    self.__clock.tick(self.__fps)
                    continue

                if self.__drop_counter != 0 and self.__drop_counter < int(round(self.__fps / 2)):
                    self.__drop_counter += 1
                    self.__clock.tick(self.__fps)
                    continue
                elif self.__drop_counter == int(round(self.__fps / 2)):
                    self.__drop_counter = 0

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if has_lost_counter == 0 and print_game_over_counter == 0:
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

            if print_game_over_counter == 0:
                self.__screen.fill(Colors.SCREEN)
                self.__all_sprites.draw(self.__screen)
                pg.display.update()
                counter += 1

            self.__clock.tick(self.__fps)

            if not running:
                pg.quit()

    def __create_frame(self):
        for i in range(0, int(self.__playing_area_right / self.__tetromino_size) + self.__tetromino_size):
            frame_block = FrameBlock(self.__screen, self.__tetromino_size)
            frame_block.rect.x = i * self.__tetromino_size
            frame_block.rect.y = -self.__tetromino_size
            self.__all_sprites.add(frame_block)
        for i in range(0, int(self.__playing_area_right / self.__tetromino_size) + self.__tetromino_size):
            frame_block = FrameBlock(self.__screen, self.__tetromino_size)
            frame_block.rect.x = i * self.__tetromino_size
            frame_block.rect.y = 21 * self.__tetromino_size + self.__tetromino_size
            self.__all_sprites.add(frame_block)
        for i in range(0, 22):
            frame_block = FrameBlock(self.__screen, self.__tetromino_size)
            frame_block.rect.x = 0
            frame_block.rect.y = i * self.__tetromino_size
            self.__all_sprites.add(frame_block)
        for i in range(0, 22):
            frame_block = FrameBlock(self.__screen, self.__tetromino_size)
            frame_block.rect.x = int(self.__playing_area_right / self.__tetromino_size) * self.__tetromino_size
            frame_block.rect.y = i * self.__tetromino_size
            self.__all_sprites.add(frame_block)

    def __create_tetromino(self, _number):
        current_tetromino = None
        if _number == 1:
            current_tetromino = Straight(self.__screen, self.__playing_area_bottom,
                                         self.__playing_area_left, self.__playing_area_right,
                                         self.__tetromino_size, self.__all_sprites)
        elif _number == 2:
            current_tetromino = Square(self.__screen, self.__playing_area_bottom,
                                       self.__playing_area_left, self.__playing_area_right,
                                       self.__tetromino_size, self.__all_sprites)
        elif _number == 3:
            current_tetromino = T(self.__screen, self.__playing_area_bottom,
                                  self.__playing_area_left, self.__playing_area_right,
                                  self.__tetromino_size, self.__all_sprites)
        elif _number == 4:
            current_tetromino = L(self.__screen, self.__playing_area_bottom,
                                  self.__playing_area_left, self.__playing_area_right,
                                  self.__tetromino_size, self.__all_sprites)
        elif _number == 5:
            current_tetromino = J(self.__screen, self.__playing_area_bottom,
                                  self.__playing_area_left, self.__playing_area_right,
                                  self.__tetromino_size, self.__all_sprites)
        elif _number == 6:
            current_tetromino = S(self.__screen, self.__playing_area_bottom,
                                  self.__playing_area_left, self.__playing_area_right,
                                  self.__tetromino_size, self.__all_sprites)
        elif _number == 7:
            current_tetromino = Z(self.__screen, self.__playing_area_bottom,
                                  self.__playing_area_left, self.__playing_area_right,
                                  self.__tetromino_size, self.__all_sprites)

        current_tetromino.rect.x = \
            int(self.__screen_width / 2) - \
            int((current_tetromino.image.get_width() / self.__tetromino_size) / 2) * \
            self.__tetromino_size
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

        for x in range(_tetromino.rect.x, _tetromino.rect.x + _tetromino.image.get_width(), self.__tetromino_size):
            for y in range(_tetromino.rect.y, _tetromino.rect.y + _tetromino.image.get_height(), self.__tetromino_size):
                rect = pg.rect.Rect((x, y, self.__tetromino_size, self.__tetromino_size))
                sprite = SingleBlock(self.__screen, self.__playing_area_bottom,
                                     self.__playing_area_left, self.__playing_area_right,
                                     self.__tetromino_size, self.__all_sprites, color)
                sprite.rect = rect
                does_collide, colliding_sprite = sprite.does_collide(_all_sprites)
                if does_collide and type(colliding_sprite) != FrameBlock and type(colliding_sprite) != SingleBlock:
                    _all_sprites.add(sprite)
        _tetromino.kill()

        self.__screen.fill(Colors.SCREEN)
        _all_sprites.draw(self.__screen)

    def __remove_full_rows(self, _all_sprites):
        for row in range(1, int(self.__playing_area_bottom / self.__tetromino_size) + 1):
            row_blocks_rect_list = []
            for col in range(1, int(self.__playing_area_right / self.__tetromino_size)):
                rect = pg.rect.Rect((col * self.__tetromino_size, row * self.__tetromino_size,
                                     self.__tetromino_size, self.__tetromino_size))
                sprite = SingleBlock(self.__screen, self.__playing_area_bottom,
                                     self.__playing_area_left, self.__playing_area_right,
                                     self.__tetromino_size, self.__all_sprites, Colors.TetroSquare)
                sprite.rect = rect
                does_collide, colliding_sprite = Tetromino.does_collide(sprite, _all_sprites)
                if does_collide:
                    row_blocks_rect_list.append(colliding_sprite)

            if len(row_blocks_rect_list) == 12:
                for colliding_sprite in row_blocks_rect_list:
                    colliding_sprite.kill()
                self.__drop_after_remove(_all_sprites, row * self.__tetromino_size)

        self.__screen.fill(Colors.SCREEN)
        _all_sprites.draw(self.__screen)

    def __drop_after_remove(self, _all_sprites, _row):
        self.__drop_counter = 1
        for tetromino in _all_sprites:
            if type(tetromino) != FrameBlock:
                if tetromino.rect.y < _row:

                    tetromino.move_down_force()

    @staticmethod
    def __compute_sizes():
        screen_height = int(round(pg.display.Info().current_h * (2 / 3)))
        tetromino_size = int(round(screen_height / 22))
        if tetromino_size % 2 == 0:
            tetromino_size += 1
        screen_width = tetromino_size * 12 + 2 * tetromino_size
        screen_height = tetromino_size * 20 + 2 * tetromino_size
        return tetromino_size, screen_width, screen_height

    def __print_game_over(self):
        font = pg.font.SysFont(name="Arial", size=60, bold=True)
        text_surface = font.render("Game Over!", True, Colors.RED)
        width = text_surface.get_width()
        height = text_surface.get_height()
        x = int(round(self.__screen_width / 2)) - int(round(width / 2))
        y = int(round(self.__screen_height / 3)) - int(round(height / 2))
        self.__screen.blit(text_surface, (x, y))
