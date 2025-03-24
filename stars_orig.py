"""
Author Paul Brace Feb 2025
Star class use to produce a star field where you are flying upwards
for Galaxians type space invaders game
"""
import arcade

import arcade
import random
from const import Const

class Star(arcade.Sprite):

    player_image = arcade.load_texture("images/whiteParticle.png")

    # create star class
    def __init__(self, x, y, size):
        """ initialise star at with movement set """
        super().__init__(Star.player_image, scale=size)
        self.change_y = -0.5   # Speed of movement
        self.center_x = x      # x position on screen
        self.center_y = y      # y position on screen

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        if self.center_y < -5:
            self.center_x = random.randint(10, Const.WINDOW_WIDTH - 10)
            self.center_y = Const.WINDOW_HEIGHT + 5
