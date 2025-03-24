"""
Author Paul Brace Feb 2025
Galaxians style space invader game
Written using the arcade library
"""

import random

import arcade
import pyglet
from pyglet. graphics import Batch

from defence import Defence
from player import Player
from alien import Alien
from missile import Missile
from explosions import Particle
from stars import Star
from const import Const
import grids


class GameView(arcade.Window):
    """
    The game class.
    """

    def __init__(self):

        # Call the parent class to set up the window
        super().__init__(Const.WINDOW_WIDTH, Const.WINDOW_HEIGHT, Const.WINDOW_TITLE)

        # Get display width and set screen center
        # set up the screen
        viewport = pyglet.display.get_display().get_default_screen()
        left = viewport.width // 2 - Const.WINDOW_WIDTH // 2
        top = viewport.height // 2 - Const.WINDOW_HEIGHT // 2
        self.set_location(left, top)

        #Scene to hold all the sprite lists and handle update and draw
        self.scene = arcade.Scene()

        # Create text Batches used to hold and draw text sprites
        self.score_batch = Batch()
        self.instructions = Batch()
        self.game_over = Batch()
        # Text sprites
        self.your_score = None
        self.high_score = None
        self.current_level = None
        self.inst = []
        self.go_text = []

        # SpriteList used in scene for our player and other sprite lists
        # better to update and draw everything using lists as
        # it is much faster than drawing individual sprites.
        # Used instead of creating individual sprite lists such as
        # self.player_list = arcade.SpriteList()
        # self.player_list.append(self.player)

        # List of stars
        self.scene.add_sprite_list("Stars")
        # List of lives left images
        self.scene.add_sprite_list("Lives")
        # List of scores
        self.scene.add_sprite_list("Scores")
        # List of defences
        self.scene.add_sprite_list("Defences")
        # List for aliens
        self.scene.add_sprite_list("Aliens")
        # List of bullets
        self.scene.add_sprite_list("Bullets")
        # List of bombs
        self.scene.add_sprite_list("Bombs")
        # List of particles for explosions
        self.scene.add_sprite_list("Particles")
        # List for player
        self.scene.add_sprite_list("Players")

        # Will be the player sprite
        self.player = None

        # Set the background colour
        self.background_color = arcade.csscolor.BLACK

        # Level currently being played
        self.level = 1

        # Load and set text for high score
        self.load_high_score()
        self.reset_score_line()

        # To create a pause before starting the next level
        self.next_level_pause = 0

        # Sounds and music
        self.sound_exp = arcade.load_sound("sounds/strike.wav")
        self.sound_game_over = arcade.load_sound("sounds/GameOver.wav")
        self.sound_live_lost = arcade.load_sound("sounds/lifeLost.wav")
        self.music = arcade.load_sound("sounds/AlienAttack.mp3")
        self.music_playing = None

        # Current state of game
        self.game_mode = Const.START_UP

    def load_high_score(self):
        try:
            with open("scores.txt", "r") as file:
                Player.high_score = int(file.read())
        except:
            Player.high_score = 0

    def reset_score_line(self):
        self.your_score = arcade.Text("Your score: 0",20,Const.WINDOW_HEIGHT - 20,
            arcade.color.WHITE, Const.SCORE_FONT_SIZE, batch=self.score_batch)
        self.high_score = arcade.Text(f"High score: {Player.high_score}",200,
            Const.WINDOW_HEIGHT - 20, arcade.color.WHITE, Const.SCORE_FONT_SIZE,
            batch=self.score_batch)
        self.current_level = arcade.Text("Level: 1",400, Const.WINDOW_HEIGHT - 20,
            arcade.color.WHITE, Const.SCORE_FONT_SIZE, batch=self.score_batch)

    def set_instructions(self):
        """ Create text sprites and add to the Batch"""
        self.create_stars()
        instructions = ["Press left and right arrow to move spaceship",
                        "Press Space Bar to fire",
                        "Score for hitting aliens:",
                        "     In grid = 10",
                        "     Flying = 50",
                        "     Crossing = 50",
                        "Score for hitting a bomb = 25",
                        "Score for clearing all aliens = 250"]
        y = 500
        self.inst.append(arcade.Text("Alien Attack - Instructions",150, y,
            arcade.color.YELLOW, Const.HEADING_FONT_SIZE, bold=True, batch=self.instructions,
            width=600))

        y -= 75
        for line in instructions:
            self.inst.append(arcade.Text(line,150, y, arcade.color.WHITE,
                Const.INST_FONT_SIZE, batch=self.instructions, width=600))
            y -= 40

        self.inst.append(arcade.Text("Press SPACE to start game without music, M with music",
            0, y - 40, arcade.color.AQUA, Const.INST_FONT_SIZE, batch=self.instructions,
            width=Const.WINDOW_WIDTH, align="center"))
        self.inst.append(arcade.Text("Author: Paul Brace 2025",
                                 0, y - 80, arcade.color.WHITE, Const.INST_FONT_SIZE / 1.5, batch=self.instructions,
                                 width=Const.WINDOW_WIDTH, align="center"))

    def set_game_over(self):
        """ Create text sprites and add to the Batch"""
        self.game_over = Batch()
        y = 450
        self.go_text.append(arcade.Text("GAME OVER",0, y, arcade.color.YELLOW,
            Const.HEADING_FONT_SIZE, align="center", bold=True, batch=self.game_over,
            width=Const.WINDOW_WIDTH))

        y -= 75
        self.go_text.append(arcade.Text(f"Your score: {Player.score}",0, y,
            arcade.color.WHITE, Const.HEADING_FONT_SIZE, align="center",
            batch=self.game_over, width=Const.WINDOW_WIDTH))
        y -= 75
        self.go_text.append(arcade.Text(f"You reached level: {self.level}",0, y,
            arcade.color.WHITE, Const.HEADING_FONT_SIZE, align="center",
            batch=self.game_over, width=Const.WINDOW_WIDTH))
        y -= 75
        if Player.score > Player.high_score:
            self.go_text.append(arcade.Text("Congratulations a new high score!",0, y,
                arcade.color.GREEN, Const.HEADING_FONT_SIZE, align="center",
                batch=self.game_over, width=Const.WINDOW_WIDTH))
            Player.high_score = Player.score
            # Save high score
            with open("scores.txt", "w") as file:
                file.write(str(Player.score))
        y -= 75
        self.inst.append(arcade.Text(
            "Press SPACE to start game without music, M with music",0, y,
            arcade.color.AQUA, Const.INST_FONT_SIZE, align="center",
            batch=self.game_over, width=Const.WINDOW_WIDTH))

    def create_stars(self):
        """ Creates a new starfield """
        self.scene["Stars"].clear()
        for x in range(Const.NUMBER_OF_STARS):
            star = Star(
                random.randint(10, Const.WINDOW_WIDTH - 10),
                random.randint(0, Const.WINDOW_HEIGHT),
                random.random() + 0.25
            )
            self.scene.add_sprite("Stars", star)

    def create_defences(self):
        # Create defences
        self.scene["Defences"].clear()
        for i in range(4):
            for j in range(3):
                rock = Defence((120 + i * 160 + j * 40, self.player.center_y + 40))
                self.scene.add_sprite("Defences", rock)

    def create_explosion(self, x_pos, y_pos, size, color, rate):
        # Create an explosion effect
        for i in range(0, size):
            particle = Particle(x_pos, y_pos, color, rate)
            self.scene.add_sprite("Particles", particle)
        self.sound_exp.play()

    def setup_level(self, new_game):
        """Set up a new game or the next level. Call this function to start or restart with 
        new_game = True and at each new level with new_game = False."""#

        if self.player != None:
            self.player.kill()
        # Create a new player
        self.player = Player()
        self.scene.add_sprite("Players", self.player)

        if new_game:
            # Set player scale as may have been 0 at end og game
            # self.player.scale = 1
            # Set up defence barrier
            self.create_defences()
            # Set life sprites to display
            Player.lives = Player.START_LIVES
            for i in range(Player.lives):
                life = arcade.Sprite("images/life.png")
                life.center_x = Const.WINDOW_WIDTH - 20 - (Player.START_LIVES - i) * 25
                life.center_y = Const.WINDOW_HEIGHT - 20
                self.scene.add_sprite("Lives", life)
            # Reset scores and speed for new game
            Player.score = 0
            self.your_score.text = "Your score: 0"
            self.high_score.text = f"High score: {Player.high_score}"
            self.level = 1
            Missile.bomb_level_interval = Missile.START_BOMB_INTERVAL
            Missile.bomb_speed = Missile.START_BOMB_SPEED
            Missile.bomb_interval = Missile.START_MISSILE_SPEED
            Alien.speed = Alien.START_SPEED

            self.game_mode = Const.IN_PLAY
            Alien.moving = True

        self.scene["Aliens"].clear()
        self.scene["Bombs"].clear()
        self.scene["Bullets"].clear()

        # Create Grid of aliens
        for y, row in enumerate(grids.grid_layouts[self.level % 10 - 1]):
            for x in range(0, len(row)):
                if row[x] == "x":
                    alien = Alien(y + 1, x, Alien.NORMAL)
                    self.scene.add_sprite("Aliens", alien)

        # Set timer for cross flying alien
        Alien.crossing_alien_timer = random.randint(200, 500)
        self.current_level.text = "Level: " + str(self.level   )

    def on_key_press(self, key: int, modifiers: int):
        """ User pressed a key """
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -Player.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = Player.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            if self.game_mode != Const.IN_PLAY:
                self.setup_level(True)
            elif self.player.alive:
                if Player.reload_timer == 0:
                    bullet = Missile((self.player.center_x, self.player.center_y + 24),
                                     Missile.UP)
                    self.scene.add_sprite("Bullets", bullet)
                    Player.reload_timer = Player.RELOAD_TIME
        elif key == arcade.key.M and self.game_mode != Const.IN_PLAY:
            self.setup_level(True)
            self.music_playing = self.music.play(volume=0.33, loop=True)

    def on_key_release(self, key, modifiers):
        """User has released a key."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            if self.player.change_x < 0:
                self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            if self.player.change_x > 0:
                self.player.change_x = 0

    def on_update(self, delta_time):
        """Called one every frame"""
        if Alien.moving:
            # scene will call all the updates of the sprite lists
            self.scene.update(delta_time)

            # Creates a pause so the user can only fire every set interval
            if Player.reload_timer > 0:
                Player.reload_timer -= 1

            # Check for end of level and use pause timer
            if len(self.scene["Aliens"]) == 0 and self.next_level_pause > 0:
                    self.next_level_pause -= 1
                    if self.next_level_pause == 0:
                        self.update_score(250)
                        self.level += 1
                        # reset screen and increase the number of bombs the aliens drop and speed
                        if Missile.bomb_level_interval > 20:
                            Missile.bomb_level_interval -= 3
                        if Missile.bomb_speed < -12:
                            Missile.bomb_speed = -2
                        # Increase alien speed
                        if Alien.speed < 6:
                            Alien.speed += 0.5
                        self.setup_level(False)
                        return

            if len(self.scene["Aliens"]) == 0 and self.next_level_pause == 0:
                # create a delay before setting up next level
                self.next_level_pause = Const.PAUSE

            # Has anything been hit
            if self.player.alive:
                self.test_if_player_hit()
            self.test_if_defence_hit_by_bomb()
            self.test_if_an_alien_has_hit_defence()
            self.test_if_bullet_has_hit_alien()
            self.test_if_bullet_has_hit_bomb()

            if len(self.scene["Aliens"])  > 0:
                # set a random alien to fly every fly interval
                Alien.fly_timer -= 1
                if Alien.fly_timer < 1:
                    Alien.fly_timer = Alien.FLY_INTERVAL
                    if len(self.scene["Aliens"]) > 0:
                        fly = random.randint(0, len(self.scene["Aliens"]) - 1)
                        self.scene["Aliens"][fly].start_flying(self.player.center_x, self.player.center_y)

                # create a crossing alien if timer expired
                Alien.crossing_alien_timer -= 1
                if Alien.crossing_alien_timer < 0:
                    if random.random() > 0.5:
                        alien = (Alien(0, 0, Alien.CRIGHT))
                    else:
                        alien = (Alien(0, 0, Alien.CLEFT))
                    self.scene.add_sprite("Aliens", alien)
                    Alien.crossing_alien_timer = random.randint(200, 500)

                # drop a bomb from a random alien every bomb_interval
                Missile.bomb_timer -= 1
                if Missile.bomb_timer < 1:
                    dropping = random.randint(0, len(self.scene["Aliens"]) - 1)
                    alien = self.scene["Aliens"][dropping]
                    # drop bomb from chosen alien
                    bomb = Missile((alien.center_x, alien.bottom), Missile.DOWN)
                    self.scene.add_sprite("Bombs", bomb)
                    Missile.bomb_timer = Missile.bomb_level_interval

            # Check if player has expired
            if self.player.done:
                self.player.kill()
                self.player = Player()
                self.scene.add_sprite("Player", self.player)

                # Check for game over and display score
                if Player.lives < 1:
                    # Hide player for score display
                    self.player.scale = 0
                    self.set_game_over()
                    Alien.moving = False
                    self.game_mode = Const.GAME_OVER
                    if self.music_playing != None:
                        arcade.stop_sound(self.music_playing)
                    self.sound_game_over.play(volume=.33)
                else:
                    # Reset screen for next level
                    self.setup_level(False)

    def test_if_player_hit(self):
        # Test if bomb has hit player
        hit_list = arcade.check_for_collision_with_list(
            self.player, self.scene["Bombs"])
        # only interested in first bomb to hit
        if len(hit_list) > 0:
            bomb = hit_list[0]
            bomb.remove_from_sprite_lists()
            self.create_explosion(bomb.center_x, bomb.bottom,
                                  50, Const.RED, 0.1)
            self.player.hit()
            self.scene["Lives"][0].kill()
            self.sound_live_lost.play()
            return

        # Test if alien has hit player
        hit_list = arcade.check_for_collision_with_list(
            self.player, self.scene["Aliens"])
        # only interested in first alien to hit
        if len(hit_list) > 0:
            alien = hit_list[0]
            alien.remove_from_sprite_lists()
            self.create_explosion(self.player.center_x, self.player.bottom,
                                  50, Const.RED, 0.1)
            self.scene["Lives"][0].kill()
            self.player.hit()

    def test_if_bullet_has_hit_bomb(self):
        # Test if hit a bomb
        for bullet in self.scene["Bullets"]:
            hit_list = arcade.check_for_collision_with_list(
                bullet, self.scene["Bombs"])
            # only interested in first bullet to hit
            if len(hit_list) > 0:
                bomb = hit_list[0]
                self.update_score(bomb.points)
                self.create_explosion(bomb.center_x, bomb.bottom,
                                      50, Const.PINK, 0.1)
                bomb.remove_from_sprite_lists()
                bullet.kill()

    def test_if_bullet_has_hit_alien(self):
        # Test if hit alien
        for bullet in self.scene["Bullets"]:
            hit_list = arcade.check_for_collision_with_list(
                bullet, self.scene["Aliens"])
            # only interested in first bullet to hit
            if len(hit_list) > 0:
                alien = hit_list[0]
                self.update_score(alien.points)
                alien.remove_from_sprite_lists()
                if alien.atype == Alien.NORMAL:
                    color = Const.AQUA
                else:
                    color = Const.ORCHID
                self.create_explosion(alien.center_x, alien.center_y, 50, color, 0.1)
                bullet.kill()

    def test_if_an_alien_has_hit_defence(self):
        # Test if alien has hit defences
        for alien in self.scene["Aliens"]:
            hit_list = arcade.check_for_collision_with_list(
                alien, self.scene["Defences"])
            # only interested in first to hit
            if len(hit_list) > 0:
                defence = hit_list[0]
                alien.remove_from_sprite_lists()
                if alien.atype == Alien.NORMAL:
                    color = Const.AQUA
                else:
                    color = Const.ORCHID
                self.create_explosion(alien.center_x, alien.bottom,
                                      50, color, 0.1)
                alien.remove_from_sprite_lists()
                defence.hit()

    def test_if_defence_hit_by_bomb(self):
        # Test if bomb has hit a defence
        for defence in self.scene["Defences"]:
            hit_list = arcade.check_for_collision_with_list(
                defence, self.scene["Bombs"])
            # only interested in first bomb to hit
            if len(hit_list) > 0:
                bomb = hit_list[0]
                bomb.remove_from_sprite_lists()
                self.create_explosion(bomb.center_x, bomb.bottom,
                                      50, Const.GREY, 0.1)
                defence.hit()

    def update_score(self, points):
        Player.score += points
        self.your_score.text = "Your score: " + str(Player.score)

    def on_draw(self):
        """Render the screen."""

        self.clear()

        # Code to draw other things will go here
        self.scene.draw()
        match self.game_mode:
            case Const.IN_PLAY:
                self.score_batch.draw()
            case Const.GAME_OVER:
                self.game_over.draw()
            case Const.START_UP:
                self.instructions.draw()

def main():
    """Main function"""
    window = GameView()
    window.set_instructions()
    arcade.run()


if __name__ == "__main__":
    main()