"""
Author Paul Brace Feb 2025
Missile class for Galaxians type space invader game
"""


import arcade
from const import Const

class Missile(arcade.Sprite):
    # set initial bomb interval - reduced each clear to increase the number of bombs
    START_BOMB_INTERVAL = 40
    START_BOMB_SPEED = -3
    START_MISSILE_SPEED = 12

    # speed will be increased for subsequent waves
    bomb_level_interval = START_BOMB_INTERVAL
    bomb_timer = START_BOMB_INTERVAL
    bomb_speed = START_BOMB_SPEED
    bullet_speed = START_MISSILE_SPEED

    # Missile or bomb
    UP = 0
    DOWN = 1

    def __init__(self, pos, direction):
        """ initialise Missile at position =- pos
            and set direction - up if player missile down if a bomb"""

        if direction == Missile.UP:
            image = "images/bullet.png"
            self.up = True
        else:
            image = "images/bomb.png"
            self.up = False
        super().__init__(image)

        self.center_x = pos[0]
        self.center_y = pos[1]
        self.done = False
        # Point score for hitting
        self.points = 25
        if self.up:
            self.change_y = Missile.bullet_speed
        else:
            self.change_y = Missile.bomb_speed

    def update(self, delta_time):
        # Check if moved off screen and kill if it has
        if self.up:
            if (self.center_y >= Const.WINDOW_HEIGHT + self.height):
                self.remove_from_sprite_lists()
                self.kill()
        elif (self.center_y < 20):
            self.remove_from_sprite_lists()
            self.kill()
        super().update(delta_time)
