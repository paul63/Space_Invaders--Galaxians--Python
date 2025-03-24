"""
Author Paul Brace Feb 2025
Galaxian style space invader game
Written using the arcade library
"""

import arcade

class Const:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    WINDOW_TITLE = "Alien Attack"

    PINK = arcade.color.PINK
    WHITE = arcade.color.WHITE
    RED = arcade.color.RED
    GREY = arcade.color.DAVY_GREY
    AQUA = arcade.color.AQUA
    ORCHID = arcade.color.ORCHID

    # for text messages
    SCORE_FONT_SIZE = 12
    INST_FONT_SIZE = 18
    HEADING_FONT_SIZE = 32

    # Game Pause
    PAUSE = 120

    # Game States
    START_UP = 0
    IN_PLAY = 1
    GAME_OVER = 2

    # Stars
    NUMBER_OF_STARS = 50

