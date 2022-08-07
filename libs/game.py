# -*- coding: utf-8 -*-

from random import randint
from libs.frame import *
from libs.tetrominos import *


class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.all_sprites = pg.sprite.Group()
        self.all_sprites_list = []
        pg.key.set_repeat(300, 20)

    def start(self):
        self.__create_frame()
        self.__main_loop()

    def __main_loop(self):
        is_key_up_pressed = False
        current_tetromino = None
        running = True
        counter = 0
        at_bottom_counter = 0
        while running:
            if current_tetromino is None:
                rand_int = randint(1, 7)

                if rand_int == 1:
                    current_tetromino = Straight(self.screen, self.all_sprites)
                elif rand_int == 2:
                    current_tetromino = Square(self.screen, self.all_sprites)
                elif rand_int == 3:
                    current_tetromino = T(self.screen, self.all_sprites)
                elif rand_int == 4:
                    current_tetromino = L(self.screen, self.all_sprites)
                elif rand_int == 5:
                    current_tetromino = J(self.screen, self.all_sprites)
                elif rand_int == 6:
                    current_tetromino = S(self.screen, self.all_sprites)
                elif rand_int == 7:
                    current_tetromino = Z(self.screen, self.all_sprites)

                current_tetromino.rect.x = \
                    int(SCREEN_WIDTH / 2) - \
                    int((current_tetromino.image.get_width() / TETROMINO_SIZE) / 2) * \
                    TETROMINO_SIZE
                current_tetromino.rect.y = PLAYING_AREA_TOP
                self.all_sprites.add(current_tetromino)

            elif Tetromino.would_collide(current_tetromino, self.all_sprites):
                at_bottom_counter += 1

            if at_bottom_counter == 15:
                at_bottom_counter = 0
                self.__change_tetromino_to_single_blocks(current_tetromino, self.all_sprites)
                self.__remove_full_rows(self.all_sprites)
                current_tetromino = None
                continue

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if not running:
                    pg.quit()

                else:
                    keys = pg.key.get_pressed()
                    if keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
                        pg.key.set_repeat(300, 70)
                        current_tetromino.move_left()
                        self.screen.fill(Colors.SCREEN)
                        self.all_sprites.draw(self.screen)
                    if keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:
                        pg.key.set_repeat(300, 70)
                        current_tetromino.move_right()
                        self.screen.fill(Colors.SCREEN)
                        self.all_sprites.draw(self.screen)
                    if keys[pg.K_DOWN]:
                        pg.key.set_repeat(300, 50)
                        current_tetromino.move_down()
                        self.screen.fill(Colors.SCREEN)
                        self.all_sprites.draw(self.screen)
                    if keys[pg.K_UP]:
                        if not is_key_up_pressed:
                            is_key_up_pressed = True
                            current_tetromino.rotate_right()
                            self.screen.fill(Colors.SCREEN)
                            self.all_sprites.draw(self.screen)
                    if event.type == pg.KEYUP:
                        is_key_up_pressed = False

            if running:
                keys = pg.key.get_pressed()
                if counter != 0 and counter % 25 == 0 and not keys[pg.K_DOWN]:
                    current_tetromino.move_down()
                    self.screen.fill(Colors.SCREEN)
                    self.all_sprites.draw(self.screen)
                    counter = 0

                self.all_sprites.draw(self.screen)
                pg.display.update()

                counter += 1
                self.clock.tick(25)

    def __create_frame(self):
        for i in range(0, int(PLAYING_AREA_RIGHT / TETROMINO_SIZE) + TETROMINO_SIZE):
            frame_block = FrameBlock(self.screen)
            frame_block.rect.x = i * TETROMINO_SIZE
            frame_block.rect.y = -40
            self.all_sprites.add(frame_block)
        for i in range(0, int(PLAYING_AREA_RIGHT / TETROMINO_SIZE) + TETROMINO_SIZE):
            frame_block = FrameBlock(self.screen)
            frame_block.rect.x = i * TETROMINO_SIZE
            frame_block.rect.y = 21 * TETROMINO_SIZE + 40
            self.all_sprites.add(frame_block)
        for i in range(0, 22):
            frame_block = FrameBlock(self.screen)
            frame_block.rect.x = 0
            frame_block.rect.y = i * TETROMINO_SIZE
            self.all_sprites.add(frame_block)
        for i in range(0, 22):
            frame_block = FrameBlock(self.screen)
            frame_block.rect.x = int(PLAYING_AREA_RIGHT / TETROMINO_SIZE) * TETROMINO_SIZE
            frame_block.rect.y = i * TETROMINO_SIZE
            self.all_sprites.add(frame_block)

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

        for x in range(_tetromino.rect.x, _tetromino.rect.x + _tetromino.image.get_width(), TETROMINO_SIZE):
            for y in range(_tetromino.rect.y, _tetromino.rect.y + _tetromino.image.get_height(), TETROMINO_SIZE):
                rect = pg.rect.Rect((x, y, TETROMINO_SIZE, TETROMINO_SIZE))
                sprite = SingleBlock(self.screen, _all_sprites, color)
                sprite.rect = rect
                does_collide, colliding_sprite = Tetromino.does_collide(sprite, _all_sprites)
                if does_collide and type(colliding_sprite) != FrameBlock and type(colliding_sprite) != SingleBlock:
                    _all_sprites.add(sprite)
        _tetromino.kill()

        self.screen.fill(Colors.SCREEN)
        _all_sprites.draw(self.screen)

    def __remove_full_rows(self, _all_sprites):
        for row in range(1, int(PLAYING_AREA_BOTTOM / TETROMINO_SIZE) + 1):
            row_blocks_rect_list = []
            for col in range(1, int(PLAYING_AREA_RIGHT / TETROMINO_SIZE)):
                rect = pg.rect.Rect((col * TETROMINO_SIZE, row * TETROMINO_SIZE, TETROMINO_SIZE, TETROMINO_SIZE))
                sprite = SingleBlock(self.screen, _all_sprites, Colors.TetroSquare)
                sprite.rect = rect
                does_collide, colliding_sprite = Tetromino.does_collide(sprite, _all_sprites)
                if does_collide:
                    row_blocks_rect_list.append(colliding_sprite)

            if len(row_blocks_rect_list) == 12:
                for colliding_sprite in row_blocks_rect_list:
                    colliding_sprite.kill()
                self.drop_after_remove(_all_sprites, row * TETROMINO_SIZE)

        self.screen.fill(Colors.SCREEN)
        _all_sprites.draw(self.screen)

    @staticmethod
    def drop_after_remove(_all_sprites, _row):
        for tetromino in _all_sprites:
            if type(tetromino) != FrameBlock:
                if tetromino.rect.y < _row:
                    tetromino.move_down_force()
