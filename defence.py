"""
Author Paul Brace Feb 2025
Defence class for Galaxians type space invader game
"""


import arcade

class Defence(arcade.Sprite):
    # defence boulder class
    def __init__(self, pos):
        """ initialise defence in position pos"""
        super().__init__("images/defence3.png")

        self.center_x = pos[0]
        self.center_y = pos[1] + self.height / 2
        # Used to keep all bottom postions at the same place for different height sprites
        self.absYpos = pos[1]
        # number of times hit
        self.damage = 0
        # True when hit for 1 update
        self.just_hit = False

    def hit(self):
        """ defence hit so reflect damage """
        self.damage += 1
        self.just_hit = True

    def update(self,  *args, **kwargs):
        # if just been hit the display next image in sequence or explode if 4th hit
        if self.just_hit:
            if self.damage < 4:
                self.texture = arcade.load_texture(f"images/defence{str(3 - self.damage)}.png")
                self.exploding = True
                self.just_hit = False
                self.center_y = self.absYpos + self.height / 2
            else:
                self.kill()
