"""
Author Paul Brace Feb 2025
Player class for Galaxians type space invader game
"""

import arcade
from const import Const

class Player(arcade.Sprite):
    """ Player for the game"""

    # Static variables
    # Time between firing bullets
    RELOAD_TIME = 20
    reload_timer = 0
    # Pixels to move each update
    PLAYER_MOVEMENT_SPEED = 3

    # Number of lives left
    START_LIVES = 3
    lives = 3
    # Current score
    score = 0
    # Current high score
    high_score = 0

    def __init__(self):
        """ Initialise player - no parameters"""
        self.player_image = arcade.load_texture("images/player.png")
        self.player_image_hit = arcade.load_texture("images/player_hit.png")

        super().__init__(self.player_image)

        self.center_x = Const.WINDOW_WIDTH / 2
        self.center_y = self.height - 10

        # Timer to pause after player shot
        self.timer = 0
        # alive is set to false when player hit
        self.alive = True
        # done tells main update to delete the object
        self.done = False

    def hit(self):
        """ player hit so set state and reduced lives
            timer is for animation of explosion """
        self.texture = self.player_image_hit
        self.alive = False
        self.timer = 150
        Player.lives -= 1

    def update(self, delta_time):
        if self.alive:
            # check if trying to move off side of window and stop
            if (self.center_x >= Const.WINDOW_WIDTH - self.width / 2 and self.change_x > 0) \
                or (self.center_x <= self.width / 2 and self.change_x < 0):
                    self.change_x = 0
        else:
            self.change_x = 0
            # gradually reduce size of player sprite
            self.scale = self.timer / 150
            # Keep image until timer reached 150
            self.timer -= 1
            if self.timer < 0:
                self.done = True
        super().update(delta_time)

