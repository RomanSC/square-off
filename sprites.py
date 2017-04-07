#!/usr/bin/python3
""" sprites.py | Thu, Apr 05, 2017 | Roman S. Collins
"""
import pygame as pg
import random, os

from constants import *

vec = pg.math.Vector2
pg.HWSURFACE

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg._layer = player_layer
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 30))
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

class Mob(pg.sprite.Sprite):
    def __init__(self, game, position):
        pg._layer = mob_layer
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((40, 40))
        self.image.fill(random.choice(mob_colors))
        # self.image = random.choice(mob_texture_list)
        self.face = pg.transform.scale(random.choice(mob_texture_list), (30, 30))
        #self.face = random.choice(mob_texture_list)
        self.face.convert()
        self.rect = self.image.get_rect()
        self.image.blit(self.face, self.rect)
        self.attack_damage = random.choice([0,0.5,1,1.5,2])
        self.aggro_range = random.choice([50,50,50,100,100,100,200,200,300,400])
        self.health = 200
        self.jump_delay = 750
        self.last_jump = 0

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
        # print(self.last_jump)
        self.acceleration = vec(0, mob_gravity)
        self.attack_damage = random.choice([0,0.5,1,1.5,2])

        # Screw it, I'll just blit my mob faces onto the mobs
        # self.image.blit(self.face, self.rect)

        if self.health <= 0:
            self.kill()
            self.game.player.kills += 1
            self.game.player.level += xp_rate

        # Lost health if shot
        # hits = pg.sprite.spritecollide(self, self.game.bullets_group, True, False)
        # if hits:
        #     self.health -= bullet_damage

        # hits = pg.sprite.spritecollide(self, self.game.player_group, False, False)
        # if hits:
        #     self.kill()

        # TODO:
        # Fix distance
        # Find player
        distance = self.game.player.rect.x - self.rect.x
        if distance > 0:
            self.move_right()
        elif distance < 0:
            self.move_left()

        last_pdu = abs(self.game.player.rect.y - self.rect.y)
        if self.game.player.rect.y < self.rect.y:
            pdu = abs(self.game.player.rect.y - self.rect.y)
            if pdu < last_pdu:
                self.jump()
                last_pdu = pdu

        # Limit height
        if self.rect.y < 0:
            self.rect.y = 0

        self.acceleration.x += self.velocity.x * mob_fric

        self.velocity += self.acceleration
        self.position += self.velocity + mob_acc * self.acceleration

        self.rect.midbottom = self.position

    def move_left(self):
        self.acceleration.x -= mob_acc

    def move_right(self):
        self.acceleration.x += mob_acc

    def move_up(self):
        self.acceleration.y -= mob_acc

    def move_down(self):
        self.acceleration.y += mob_acc

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms_group, False)
        self.rect.x -= 1
        if hits:
            now = pg.time.get_ticks()
            if now - self.last_jump > self.jump_delay:
                self.velocity.y += -20


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg._layer = platform_layer
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(platform_color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# TODO:
# Bullets (maybe)

# class Bullet(pg.sprite.Sprite):
#     def __init__(self):
#         pass
