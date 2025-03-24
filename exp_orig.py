"""
Author Paul Brace Feb 2025
Explosion class for Galaxians type space invaders game
"""
from math import factorial

import arcade
import random

FRICTION = 0.99

class Particle(arcade.Sprite):

    def __init__(self, x, y, color, velocity_x, velocity_y, rate):
        """ X, y = center of explosion
            color = color of particles
            velocity is speed that the particle moves away from center
            rate is the speed that the particle shrinks"""
        super().__init__(f"images/{color}Particle.png", soft=True)
        self.center_x = x
        self.center_y = y
        self.radius = 10
        self.change_x = velocity_x
        self.change_y = velocity_y
        self.rate = rate

    def update(self, *args, **kwargs):
        # change velocity
        self.change_x *= FRICTION
        self.change_y *= FRICTION
        # Reduce in size so shrinks with time
        if self.radius > 0:
            self.radius -= self.rate
            self.scale = self.radius / 10 * 1.25
        if self.radius <= 0:
            self.kill()
        super().update( *args, **kwargs)
