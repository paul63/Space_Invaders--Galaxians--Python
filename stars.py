"""
Author Paul Brace Feb 2025
Star class use to produce a star field where you are flying upwards
for Galaxians type space invaders game
"""
import arcade

import arcade
import random
from const import Const

class Star(arcade.SpriteCircle):

        # create star class
    def __init__(self, x, y, size):
        """ initialise star at with movement set """
        super().__init__(2, Const.WHITE)
        self.change_y = -0.5   # Speed of movement
        self.center_x = x      # x position on screen
        self.center_y = y      # y position on screen
        self.scale = size
        self.alpha = random.randint(100, 255)

    def update(self, delta_time) -> None:
        super().update(delta_time)
        if self.center_y < -5:
            self.center_x = random.randint(10, Const.WINDOW_WIDTH - 10)
            self.center_y = Const.WINDOW_HEIGHT + 5
