""" player.py | Tue, Apr 04, 2017 | Roman S. Collins
"""
import pygame as pg
import random, os

from constants import *

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg._layer = player_layer
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(blue)
        self.rect = self.image.get_rect()

        # Center the player
        self.rect.center = (screen_width/2, screen_height/2)

        self.position = (screen_width/2, screen_height/2)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.last_jump = 0
        self.last_double_jump = 0
        self.jump_delay = 250
        # self.jumps = 2
        self.allow_move = True
        self.floor_solid = True
        self.allow_jump = False
        # print(dir(self.position))
        # print(dir(self.rect.center))

        # Last time shot bullet
        self.last_shot = 0
        self.rotation = 0
        self.shoot_position = (self.position[0] - 30, self.position[1])

        # Health and health bar
        self.max_hp = 100 # Players max hp
        self.cur_hp = self.max_hp # Starting current hp
        self.hp_bar_str = "{} / {}".format(self.max_hp, self.cur_hp)

        self.defense = random.choice([0,0.5,1,1.5,2,2.5,3])

        self.lives = 5
        self.level = 1

        # TODO:
        # Amount of kills and update level
        # related  to kills in self.update()
        self.kills = 0

    # TODO:
    # Player names
    def __str__(self):
        return "Player"

    def update(self):
        # self.volacity_x, self.volacity_y = 0, 0
        self.acceleration = vec(0, player_gravity)

        self.defense = random.choice([0,0.5,1,1.5,2,2.5,3])

        self.player_controls()

        # Apply friction
        self.acceleration.x += self.velocity.x * player_fric

        # Equations for motion
        self.velocity += self.acceleration
        self.position += self.velocity + player_acc * self.acceleration

        self.shoot_position = (self.position.x - 15, self.position.y)

        self.rect.midbottom = self.position

        if self.rect.right >= screen_width:
            self.rect.left = 20

        if self.rect.left <= 0:
            self.rect.right = screen_width - 20

        if self.rect.y > screen_height:
            self.center()

        if self.cur_hp <= 0:
            self.lives -= 1

    def player_controls(self):
        keystate = pg.key.get_pressed()

        if keystate[pg.K_LEFT] or keystate[pg.K_a]:
            self.move_left()

        if keystate[pg.K_RIGHT] or keystate[pg.K_d]:
            self.move_right()

        # TODO
        # Convert to some other control
        # if keystate[pg.K_UP] or keystate[pg.K_w] and self.allow_move:
        #     self.move_up()

        # TODO
        # Make fall through floors
        # if keystate[pg.K_DOWN] or keystate[pg.K_s] and self.allow_move:
        #      self.floor_solid = False
        #     self.move_down()

        # if keystate[pg.K_t]:
        #     self.center()

    def move_left(self):
        if self.allow_move:
            self.acceleration.x -= player_acc

    def move_right(self):
        if self.allow_move:
            self.acceleration.x += player_acc

    def move_up(self):
        if self.allow_move:
            self.acceleration.y -= player_acc

    def move_down(self):
        if self.allow_move:
            self.acceleration.y += player_acc

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms_group, False)
        self.rect.x -= 1
        if hits:
            self.velocity.y += -20
            self.last_jump = pg.time.get_ticks()
            # self.jumps = 2
            self.allow_jump = True


    def double_jump(self):
        # TODO:
        # Skill based maximum double jumps
        now = pg.time.get_ticks()
        if now - self.last_jump > self.jump_delay and self.allow_jump:
            self.velocity.y += -15
            self.allow_jump = False
        self.last_double_jump = now

    def center(self):
        self.rect.center = (screen_width/2, screen_height/2)

