# -*- coding: utf-8 -*-


from libs.game import *
from libs.menu import *

import pygame as pg


if __name__ == "__main__":
    pg.init()
    pg.display.set_caption('PyTetro')
    all_sprites = pg.sprite.Group()
    constants = Constants()
    window = pg.display.set_mode((constants.window_width * 1.5, constants.window_height))
    frame = Frame(constants, all_sprites)
    frame.create_frame()

    selected_difficulty = 1

    do_run = True
    while do_run:
        main_menu = MainMenu(window, constants, all_sprites)
        menu_choice = main_menu.show_main_menu()
        if menu_choice == -1:
            do_run = False
            pg.quit()
        elif menu_choice == 1:
            difficulty_menu = DifficultyMenu(window, constants, all_sprites, selected_difficulty)
            selected_difficulty = difficulty_menu.show_difficulty_menu()
            if selected_difficulty == -1:
                do_run = False
                pg.quit()
        else:
            game = Game(window, constants, all_sprites, selected_difficulty)
            if not game.start():
                do_run = False
