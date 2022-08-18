# -*- coding: utf-8 -*-


class Constants:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    SCREEN = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 102, 255)
    LIGHT_RED = (255, 153, 153)


class Menu:
    class MenuItem:
        bg_unselected = Constants.RED
        bg_selected = Constants.LIGHT_RED
        text = Constants.WHITE


class Frame:
    # Grey:
    class FrameBlock:
        bg_topleft = (217, 217, 217)
        bg_bottomright = (77, 77, 77)
        fg_square = (128, 128, 128)


class Tetrominos:
    # Blue:
    class Straight:
        bg_topleft = (128, 179, 255)
        bg_bottomright = (0, 51, 128)
        fg_square = (0, 102, 255)

    # Green:
    class Square:
        bg_topleft = (128, 255, 170)
        bg_bottomright = (0, 128, 43)
        fg_square = (0, 153, 51)

    # Orange:
    class T:
        bg_topleft = (255, 204, 128)
        bg_bottomright = (153, 92, 0)
        fg_square = (255, 153, 0)

    # Red:
    class L:
        bg_topleft = (255, 179, 179)
        bg_bottomright = (153, 0, 0)
        fg_square = (255, 26, 26)

    # Yellow:
    class J:
        bg_topleft = (255, 255, 179)
        bg_bottomright = (153, 153, 0)
        fg_square = (255, 255, 0)

    # Cyan:
    class S:
        bg_topleft = (179, 255, 255)
        bg_bottomright = (0, 102, 102)
        fg_square = (0, 230, 230)

    # Purple:
    class Z:
        bg_topleft = (255, 179, 255)
        bg_bottomright = (77, 0, 77)
        fg_square = (179, 0, 179)
