"""
Author Paul Brace Feb 2025
Explosion class for Galaxians type space invaders game
"""
from math import factorial

import arcade
import random
import math

from arcade.csscolor import GREY

from const import Const

FRICTION = 0.99
FADE_RATE = 4

# Start scale of smoke, and how fast is scales up
SMOKE_START_SCALE = 0.25
SMOKE_EXPANSION_RATE = 0.03

# Rate smoke fades, and rises
SMOKE_FADE_RATE = 8
SMOKE_RISE_RATE = 0.25

# Chance we leave smoke trail
SMOKE_CHANCE = 0.025


class Smoke(arcade.SpriteCircle):
    """Particle with smoke like behavior."""
    def __init__(self, size):
        super().__init__(size, arcade.color.LIGHT_GRAY, soft=True)
        self.change_y = SMOKE_RISE_RATE
        self.scale = SMOKE_START_SCALE

    def update(self, *args, **kwargs):
        """Update this particle"""
        if self.alpha <= SMOKE_FADE_RATE:
            # Remove faded out particles
            self.remove_from_sprite_lists()
        else:
            # Update values
            self.alpha -= int(SMOKE_FADE_RATE)
            self.add_scale(SMOKE_EXPANSION_RATE)
            super().update(*args, **kwargs)


class Particle(arcade.SpriteCircle):

    def __init__(self, x, y, color, rate):
        """ X, y = center of explosion
            color = color of particles
            velocity is speed that the particle moves away from center
            rate is the speed that the particle shrinks"""
        super().__init__(3, color)
        self.position = (x, y)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.random() * 2
        self.change_x = math.sin(angle) * speed
        self.change_y = math.cos(angle) * speed
        self.rate = -rate / 8
        self.scale = 1
        self.alpha = 255

    def update(self, delta_time):
        if self.alpha <= 0 or self.scale[0] <= 0:
            self.remove_from_sprite_lists()
        else:
            # change velocity to slow down particle
            self.change_x *= FRICTION
            self.change_y *= FRICTION
            # Increase transparency
            self.alpha -= FADE_RATE
            # Reduce in size so shrinks with time
            self.add_scale(self.rate)

            # Leave a smoke particle?
            if random.random() <= SMOKE_CHANCE:
                smoke = Smoke(5)
                smoke.position = self.position
                # Add a smoke particle to the sprite_list this sprite is in
                self.sprite_lists[0].append(smoke)
                # Change the colour of the particle
                red = random.randint(126, 255)
                green = random.randint(0, red)
                blue = 0
                self.color = (red, green, blue)

            super().update(delta_time)
