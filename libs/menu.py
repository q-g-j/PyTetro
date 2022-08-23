# -*- coding: utf-8 -*-


import libs.colors as colors
from libs.fonts import *
from libs.constants import *


class MainMenuItem:
    def __init__(self, _window: pg.Surface, _constants: Constants, _offset_y: int, _text: str):
        self.color = colors.MenuItem.bg_unselected
        self.__window = _window
        self.__constants = _constants
        self.__offset_y = _offset_y
        self.__text = _text
        self.__fonts = Fonts(self.__constants)
        self.is_selected = False

        self.__width = int(round(_constants.window_width / 2))
        self.__height = int(round(self.__width / 5))
        if self.__height % 2 != 0:
            self.__height += 1
        self.__border_radius = int(self.__height / 2)
        self.__left = int(round(_constants.window_width / 2 - self.__width / 2))
        self.__top = int(
            round(_constants.window_height / 5)) + (self.__height + int(round(self.__height / 2))) * _offset_y

    def draw(self):
        pg.draw.rect(self.__window, self.color,
                     (self.__left, self.__top, self.__width, self.__height), border_radius=self.__border_radius)
        text_surface = self.__fonts.main_menu_item.render(self.__text, True, colors.MenuItem.text)
        width = text_surface.get_width()
        height = text_surface.get_height()
        x = self.__left + int(round(self.__width / 2) - int(round(width / 2)))
        y = self.__top + int(round(self.__height / 2) - int(round(height / 2)))
        self.__window.blit(text_surface, (x, y))


class MainMenu:
    def __init__(self, _window: pg.Surface, _constants: Constants, _all_sprites: pg.sprite.Group):
        self.__window = _window
        self.__constants = _constants
        self.__all_sprites = _all_sprites
        self.__clock = pg.time.Clock()

        pg.key.set_repeat(200, 100)

        self.__menu_items = [
            MainMenuItem(self.__window, self.__constants, 0, "new game"),
            MainMenuItem(self.__window, self.__constants, 1, "level"),
            MainMenuItem(self.__window, self.__constants, 2, "quit")
            ]

    def show_main_menu(self):
        return self.__main_menu_loop()

    def __main_menu_loop(self):
        selected_menu_item = 0
        self.__menu_items[0].is_selected = True
        self.__menu_items[0].color = colors.MenuItem.bg_selected
        do_quit = False
        is_running = True
        while is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    is_running = False
                    do_quit = True
                elif event.type == pg.KEYDOWN:
                    pressed_keys = pg.key.get_pressed()
                    if pressed_keys[pg.K_DOWN] or pressed_keys[pg.K_k]:
                        if selected_menu_item < 2:
                            selected_menu_item += 1
                            self.__menu_items[selected_menu_item].is_selected = True
                            self.__menu_items[selected_menu_item].color = colors.MenuItem.bg_selected
                            self.__menu_items[selected_menu_item - 1].is_selected = False
                            self.__menu_items[selected_menu_item - 1].color = colors.MenuItem.bg_unselected

                    elif pressed_keys[pg.K_UP] or pressed_keys[pg.K_i]:
                        if selected_menu_item > 0:
                            selected_menu_item -= 1
                            self.__menu_items[selected_menu_item].is_selected = True
                            self.__menu_items[selected_menu_item].color = colors.MenuItem.bg_selected
                            self.__menu_items[selected_menu_item + 1].is_selected = False
                            self.__menu_items[selected_menu_item + 1].color = colors.MenuItem.bg_unselected
                    elif pressed_keys[pg.K_RETURN] or pressed_keys[pg.K_KP_ENTER]:
                        for index in range(len(self.__menu_items)):
                            if self.__menu_items[index].is_selected:
                                if index == 0:
                                    return 0
                                elif index == 1:
                                    return 1
                                elif index == 2:
                                    is_running = False
                                    do_quit = True

            if is_running:
                self.__window.fill(colors.Constants.SCREEN)
                for menu_item in self.__menu_items:
                    menu_item.draw()
                self.__all_sprites.draw(self.__window)
                pg.display.update()

            if is_running:
                self.__clock.tick(60)

            if do_quit:
                return -1


class LevelSelectorFrame:
    def __init__(self, _window: pg.Surface, _constants: Constants):
        self.__window = _window
        self.__constants = _constants

    def draw(self):
        width = int(round(self.__constants.window_width / 5))
        height = int(round(self.__constants.window_height / 10))
        x = int(self.__constants.window_width / 2 - width / 2)
        y = int(self.__constants.window_height / 2 - height / 2)
        pg.draw.rect(self.__window, (255, 200, 0), (x, y, width, height), 6, border_radius=int(height / 3))


class LevelNumber:
    def __init__(self, _window: pg.Surface, _constants: Constants, _number: int):
        self.__window = _window
        self.__constants = _constants
        self.__number = _number
        self.__fonts = Fonts(self.__constants)

        self.position = 0

    def draw(self):
        text_surface = self.__fonts.level_number.render(str(self.__number), True, colors.MenuItem.text)
        width = text_surface.get_width()
        height = text_surface.get_height()
        offset_y = self.position * height
        x = int(round(self.__constants.window_width / 2) - int(round(width / 2)))
        y = int(round(self.__constants.window_height / 2) - int(round(height / 2))) + offset_y
        self.__window.blit(text_surface, (x, y))


class LevelMenu:
    def __init__(self, _window: pg.Surface, _constants: Constants, _all_sprites: pg.sprite.Group,
                 _last_selected_level: int):
        self.__window = _window
        self.__constants = _constants
        self.__all_sprites = _all_sprites
        self.__level = _last_selected_level
        self.__clock = pg.time.Clock()

        self.__level_selector_frame = LevelSelectorFrame(self.__window, self.__constants)
        self.__level_numbers = list()
        for i in range(1, self.__constants.max_level + 1):
            number = LevelNumber(self.__window, self.__constants, i)
            self.__level_numbers.append(number)

    def show_level_menu(self) -> int:
        return self.__level_menu_loop()

    def __level_menu_loop(self) -> int:
        do_quit = False
        is_running = True
        while is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    is_running = False
                    do_quit = True
                elif event.type == pg.KEYDOWN:
                    pressed_keys = pg.key.get_pressed()
                    if pressed_keys[pg.K_DOWN] or pressed_keys[pg.K_k]:
                        if self.__level < self.__constants.max_level:
                            self.__level += 1
                    elif pressed_keys[pg.K_UP] or pressed_keys[pg.K_i]:
                        if self.__level > 1:
                            self.__level -= 1
                    elif pressed_keys[pg.K_RETURN] or pressed_keys[pg.K_KP_ENTER]:
                        return self.__level

            if is_running:
                self.__window.fill(colors.Constants.SCREEN)
                self.__level_selector_frame.draw()

                if self.__level == 1:
                    self.__level_numbers[self.__level - 1].position = 0
                    self.__level_numbers[self.__level - 1].draw()

                    self.__level_numbers[self.__level].position = 1
                    self.__level_numbers[self.__level].draw()
                elif 1 < self.__level < self.__constants.max_level:
                    self.__level_numbers[self.__level - 2].position = -1
                    self.__level_numbers[self.__level - 2].draw()

                    self.__level_numbers[self.__level - 1].position = 0
                    self.__level_numbers[self.__level - 1].draw()

                    self.__level_numbers[self.__level].position = 1
                    self.__level_numbers[self.__level].draw()
                elif self.__level == self.__constants.max_level:
                    self.__level_numbers[self.__level - 2].position = -1
                    self.__level_numbers[self.__level - 2].draw()

                    self.__level_numbers[self.__level - 1].position = 0
                    self.__level_numbers[self.__level - 1].draw()

                self.__all_sprites.draw(self.__window)
                pg.display.update()

            if is_running:
                self.__clock.tick(self.__constants.fps)

            if do_quit:
                return -1
