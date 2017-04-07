""" mob.py | Tue, Apr 04, 2017 | Roman S. Collins
"""
import pygame as pg
import random, os

from constants import *

# TODO:
# Move to constants
vec = pg.math.Vector2

class Mob(pg.sprite.Sprite):
    def __init__(self, game, position):
        pg._layer = mob_layer
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.attack_damage = random.choice([0,0.5,1,1.5,2])
        self.aggro_range = 20
        self.health = 200

        # TODO:
        # Improve starting location
        # Use while loop to make sure mobs
        # do not spawn on top of player directly
        # to prevent player from instantly dying
        # at beginning of the game
        # self.rect.x = x
        # self.rect.y = y

        self.position = position
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

    # TODO:
    # Mob names
    def __str__(self):
        return "Mob"

    # TODO
    def update(self):
        self.acceleration = vec(0, mob_gravity)
        self.attack_damage = random.choice([0,0.5,1,1.5,2])

        # TODO
        # Improve this
        # Find the player and kill em
        # for i in range(self.aggro_range):
        #     self.rect.x += i
        #     found = pg.sprite.spritecollide(self.game.player, self.game.mobs_group, False)
        #     self.rect.x -= i
        #     if found:
        #         print("FOUND:")
        #         print(self.game.player.rect.x, self.game.player.rect.y)
        #         if self.rect.right < self.game.player.rect.left:
        #             self.move_x(right=True)
        #         elif self.rect.left > self.game.player.rect.right:
        #             self.move_x(left=True)
        #     found = None
        # print(self.rect.left - self.game.player.rect.right)
        # print(self.rect.left - self.game.player.rect.right)

        if self.health <= 0:
            self.kill()
            self.game.player.kills += 1
            self.game.player.level += xp_rate

        hits = pg.sprite.spritecollide(self, self.game.bullets_group, True, False)
        if hits:
            self.health -= bullet_damage

        if self.rect.right - self.game.player.rect.x < random.randint(5, self.aggro_range):
            self.move_right()
        elif self.rect.left - self.game.player.rect.x > random.randint(5, self.aggro_range):
            self.move_left()

        self.acceleration.x += self.velocity.x * mob_fric

        self.velocity += self.acceleration
        self.position += self.velocity + mob_acc * self.acceleration

        self.rect.midbottom = self.position

        # TODO:
        # Fix me
        # Zero out velocity when mob hits a platform
        # self.rect.x += 1
        # hits = pg.sprite.spritecollide(self, self.game.platforms_group, False)
        # self.rect.x -= 1
        # if hits:
        #     self.velocity.y += -20

        # Find the player

    def move_left(self):
        self.acceleration.x -= mob_acc

    def move_right(self):
        self.acceleration.x += mob_acc

    def move_up(self):
        self.acceleration.y -= mob_acc

    def move_down(self):
        self.acceleration.y += mob_acc


