"""
Author Paul Brace Feb 2025
Alien class for Galaxians type space invaders game
"""

import arcade
from const import Const
import math

def path(p0, p1, p2, t):
    # return position on bezier curve based on t = 0 for start 1 = end
    px = p0[0] * (1 - t) ** 2 + 2 * (1 - t) * t * p1[0] + p2[0] * t ** 2
    py = p0[1] * (1 - t) ** 2 + 2 * (1 - t) * t * p1[1] + p2[1] * t ** 2
    return px, py

class Alien(arcade.Sprite):
    # Create alien class
    # static variables
    # Alient types
    NORMAL = 0
    CLEFT = 1
    CRIGHT = 2
    FLYING = 3

    moving = False
    START_SPEED = 3
    speed = START_SPEED
    # frames between setting a random alien flying
    FLY_INTERVAL = 200
    fly_timer = FLY_INTERVAL
    # counter to next crossing alien appearance
    special_alien_timer = 1

    # frames between wings moving
    FLAP_SPEED = 10
    # Images used for animation
    normal_flap_0 = arcade.load_texture('images/alien11.png')
    normal_flap_1 = arcade.load_texture('images/alien12.png')
    special_flap_0 = arcade.load_texture('images/alien01.png')
    special_flap_1 = arcade.load_texture('images/alien02.png')

    def __init__(self, start_row, col_number, atype):
        # aType normal = standard alien in grid
        # cleft = moving from right to x at y of screen
        # else = moving x to right at y of screen
        self.atype = atype
        if atype == Alien.NORMAL:
            """ initialise at row and column """
            super().__init__(self.normal_flap_0)
            self.center_y = Const.WINDOW_HEIGHT - start_row * self.height * 1.5
            self.center_x = 175 + col_number * self.width * 1.25
            if Alien.moving:
                self.change_x = Alien.speed
            self.flap_0 = self.normal_flap_0
            self.flap_1 = self.normal_flap_1
            self.points = 10
        else:
            """ initialise for crossing """
            super().__init__(self.special_flap_0)
            self.flap_0 = self.special_flap_0
            self.flap_1 = self.special_flap_1
            self.center_y = Const.WINDOW_HEIGHT - 40
            self.points = 50
            if atype == Alien.CLEFT:
                # special alien crossing right to left
                self.center_x = Const.WINDOW_WIDTH
                self.change_x = -Alien.speed
            else:
                # special alien crossing left to right
                self.center_x = 0
                self.change_x = Alien.speed
        self.timer = 10 # Alien.FLAP_SPEED
        # alive set to false when alien hit
        self.alive = True
        # set variables used if alien flying
        self.start = 0, 0
        self.end = 0, 0
        self.mid = 0, 0
        self.fly_delta = 0
        self.fly_pos = 0

    def update(self, delta_time):
        """ check for image change and move if game in progress """
        if self.change_x == 0 and Alien.moving:
            self.change_x = Alien.speed
        super().update(delta_time)
        if self.alive:
            # if alien is flying will move following a bezier curve
            # so override center_x and center_y positions Kill alien if moved off screen
            if self.atype == Alien.FLYING:
                self.fly_pos += self.fly_delta
                self.center_x, self.center_y = path(self.start, self.mid, self.end, self.fly_pos)
                if self.center_y < self.height / 2:
                    self.kill()
            elif self.atype == Alien.NORMAL:
                if (self.center_x < self.width / 2 and self.change_x < 0) or \
                   (self.center_x > Const.WINDOW_WIDTH - self.width / 2 and self.change_x > 0):
                    self.move_down()
            else:
                if (self.center_x < 0 - self.width and self.change_x < 0) or \
                   (self.center_x > Const.WINDOW_WIDTH + self.width and self.change_x > 0):
                    self.kill()

        self.change_image()

    def move_down(self):
        """ used when reached side of screen move down and reverse direction """
        self.change_x *= -1
        self.center_y -= self.height / 1.5
        if self.center_y < self.height / 2:
            self.kill()

    def change_image(self):
        """ if still alive change image each flap period"""
        if self.alive:
            self.timer -= 1
            if self.timer < 1:
                self.timer = Alien.FLAP_SPEED
                if self.texture == self.flap_0:
                    self.texture = self.flap_1
                else:
                    self.texture = self.flap_0

    def start_flying(self, x, y):
        # set the alien flying on a bezier curve from current position to target position x:y
        # Ignore if already flying
        if self.atype == Alien.FLYING:
            return
        self.atype = Alien.FLYING
        self.flap_0 = self.special_flap_0
        self.flap_1 = self.special_flap_1
        # Set control points
        self.start = (self.center_x, self.center_y)
        self.end = (x, y)
        if self.center_x < Const.WINDOW_WIDTH // 2:
            # self.mid = (random.randint(1, 100), random.randint(1, 100))
            self.mid = (1, Const.WINDOW_HEIGHT - 1)
        else:
            self.mid = (Const.WINDOW_WIDTH, Const.WINDOW_HEIGHT - 1)
            # self.mid = (random.randint(WIDTH - 100, WIDTH), random.randint(1, 100))
        # calculate distance to player
        self.fly_delta = 2 / math.sqrt(pow((x - self.center_x), 2) + pow((y - self.center_y), 2))
        self.fly_pos = 0

