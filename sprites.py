#!/usr/bin/python3
""" sprites.py | Thu, Apr 05, 2017 | Roman S. Collins
"""
import pygame as pg
import random, os

from constants import *

vec = pg.math.Vector2

import math

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg._layer = player_layer
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 30))
        self.image.fill(blue)
        self.rect = self.image.get_rect()

        # Center the player on the screen
        self.rect.center = (screen_width/2, screen_height/2)

        self.position = (screen_width/2, screen_height/2)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.last_jump = 0
        self.last_floor = 0
        self.last_double_jump = 0
        self.jump_delay = 250
        self.floor_solid = True
        self.allow_jump = False

        # print(dir(self.position))
        # print(dir(self.rect.center))

        # Health and health bar
        self.max_hp = 100 # Players max hp
        self.cur_hp = self.max_hp # Starting current hp
        self.hp_bar_str = "{} / {}".format(self.max_hp, self.cur_hp)

        self.lives = 99
        self.level = 1

        # TODO:
        # Amount of kills and update level
        # related  to kills in self.update()
        self.kills = 0

        # Center the player on the screen
        self.rect.center = (screen_width/2, screen_height/2)

        # Shooting
        self.last_shot = 0

    # TODO:
    # Player names
    def __str__(self):
        return "Player"

    def update(self):
        # self.volacity_x, self.volacity_y = 0, 0

        # Gravity
        self.acceleration = vec(0, player_gravity)

        self.defense = random.choice([0,0.5,1,1.5])

        self.player_controls()

        # Apply friction
        self.acceleration.x += self.velocity.x * player_fric

        # Equations for motion
        self.velocity += self.acceleration
        self.position += self.velocity + player_acc * self.acceleration

        self.rect.midbottom = self.position

        if self.cur_hp <= 0:
            self.lives -= 1

    def player_controls(self):
        keystate = pg.key.get_pressed()

        if keystate[pg.K_LEFT] or keystate[pg.K_a]:
            self.move_left()

        if keystate[pg.K_RIGHT] or keystate[pg.K_d]:
            self.move_right()

        if keystate[pg.K_UP] or keystate[pg.K_w]:
            self.move_up()

        # TODO
        # Make fall through floors
        # if keystate[pg.K_DOWN] or keystate[pg.K_s] and self.allow_move:
        #     self.floor_solid = False
        #     self.move_down()

        if keystate[pg.K_SPACE]:
        #if pg.key.get_pressed()[32] == 1:
            self.jump()
            self.double_jump()

        if keystate[pg.K_t]:
            self.center()

        if pg.mouse.get_pressed()[0] == 1:
            now = pg.time.get_ticks()
            if now - self.last_shot > bullet_rate:
                b = Bullet(self.game)
                self.game.bullets_group.add(b)
                self.game.all_sprites_group.add(b)
                self.last_shot = now

    def move_left(self):
        self.acceleration.x -= player_acc

    def move_right(self):
        self.acceleration.x += player_acc

    def move_up(self):
        if not self.rect.y <= 1:
            self.acceleration.y -= player_acc

    def move_down(self):
        if not self.rext.y >= screen_height - 1:
            self.acceleration.y += player_acc

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self,
                                       self.game.\
                                       platforms_group,
                                       False)
        self.rect.x -= 1

        if hits:
            now = pg.time.get_ticks()
            self.last_floor = now
            if now - self.last_jump > self.jump_delay:
                if now - self.last_double_jump > 50:
                    self.velocity.y += -18
                    self.last_jump = pg.time.get_ticks()
                    self.allow_jump = True

    def double_jump(self):
        # TODO:
        # Skill based maximum double jumps
        now = pg.time.get_ticks()

        if now - self.last_jump > self.jump_delay \
        and self.allow_jump:

            self.velocity.y += -20
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
        self.face = pg.transform.scale(random.choice(mob_texture_list),
                                      (30, 30))
        #self.face = random.choice(mob_texture_list)
        self.face.convert()
        self.rect = self.image.get_rect()
        self.image.blit(self.face, self.rect)
        self.attack_damage = random.choice(MOB_ATTACK_DAMAGE)
        self.aggro_range = 250
        self.health = 20
        self.jump_delay = 750
        self.last_jump = 0
        # For self.back_forth()
        self.last_back_forth = 0

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

        # self.move_options = [True, False]
        # self.move_freely = random.choice(self.move_options)

#         move_choice = random.choice([1, 2, 3, 4, 5, 6, 7, 8])
#         if move_choice <= 3:
#             self.move_freely = False
#         elif move_choice >= 4:
#             self.move_freely = True

        self.movement_style = random.choice([1, 2, 3, 4,
                                            5, 6, 7, 8,
                                            9, 10])

        # Distance from player
        self.dpx = self.game.player.rect.x - self.rect.x
        self.dpy = self.game.player.rect.y - self.rect.y

        # Distance from screen edges
        self.distance_edge_left_x = (0 - self.rect.x)
        self.distance_edge_right_x = (screen_width - self.rect.x)
        self.distance_edge_top_y = (0 - self.rect.y)
        self.distance_edge_bottom_y = (screen_height - self.rect.y)


        # Back and forth left right distance
        self.movement_range = random.choice(MOB_BF_RANGE)
        self.cur_range = 0
        self.lr = "l"

        self.friction = -abs(MOB_FRIC)

    # TODO:
    # Mob names
    def __str__(self):
        return "Mob"

    # TODO
    def update(self):
        # print(self.last_jump)
        self.acceleration = vec(0, mob_gravity)
        self.attack_damage = random.choice([0,0.5,1,1.5,2])

        # Distance from player
        self.dpx = self.game.player.rect.x - self.rect.x
        self.dpy = self.game.player.rect.y - self.rect.y

        # Distance from screen edges
        self.distance_edge_left_x = (0 - self.rect.x)
        self.distance_edge_right_x = (screen_width - self.rect.x)
        self.distance_edge_top_y = (0 - self.rect.y)
        self.distance_edge_bottom_y = (screen_height - self.rect.y)

        # print("<-- Distance from left edge: ", self.distance_edge_left_x)
        # print("<-- Distance from right edge: ", self.distance_edge_right_x)
        # print(self.distance_edge_top_y)
        # print(self.distance_edge_bottom_y)

        # print(abs(self.distance_edge_left_x))
        # print(abs(self.distance_edge_right_x))
        # print(abs(self.distance_edge_top_y))
        # print(abs(self.distance_edge_bottom_y))

        if self.health <= 0:
            self.kill()
            self.game.player.kills += 1
            self.game.player.level += xp_rate

            if self.game.player.cur_hp < self.game.player.max_hp:
                gen_hp_reward = random.choice(MOB_HP_REWARD)
                if gen_hp_reward > 0:
                    self.game.player.cur_hp += gen_hp_reward

        # Lost health if shot
        hits = pg.sprite.spritecollide(self,
                                       self.game.bullets_group,
                                       True,
                                       False)
        if hits:
            self.health -= bullet_damage * self.game.player.level

        # hits = pg.sprite.spritecollide(self,
        #                                self.game.player_group,
        #                                False,
        #                                False)
        # if hits:
        #     self.kill()

        # if self.move_freely:
        #     self.free_move()
        # elif not self.move_freely:
        #     # TODO function to make mobs move back and forth
        #     self.back_forth()

        if self.movement_style <= 4:
            self.free_move()
        elif self.movement_style <= 8:
            self.back_forth()
        elif self.movement_style <= 10:
            self.free_move_jump()
        else:
            self.back_forth()

        # TODO:
        # Fix distance
        # Find player
        # distance = self.game.player.rect.x - self.rect.x
        # if distance > 0:
        #     self.move_right()
        # elif distance < 0:
        #     self.move_left()

        # last_pdu = abs(self.game.player.rect.y - self.rect.y)
        # if self.game.player.rect.y < self.rect.y:
        #     pdu = abs(self.game.player.rect.y - self.rect.y)
        #     if pdu < last_pdu:
        #         self.jump()
        #         last_pdu = pdu

        # Limit height and width
        if self.rect.y - (screen_height / 2) > screen_height:
            self.kill()
        if self.rect.x - (screen_width / 2) > screen_width:
            self.kill()

        self.acceleration.x += self.velocity.x * self.friction

        self.velocity += self.acceleration
        self.position += self.velocity + mob_acc * self.acceleration

        self.rect.midbottom = self.position

    def move_left(self):
        # print(self.distance_edge_left_x)
        if self.distance_edge_left_x < 0:
            self.acceleration.x -= mob_acc

    def move_right(self):
        # print(self.distance_edge_right_x)
        if self.distance_edge_right_x > 0:
            self.acceleration.x += mob_acc

    # def move_up(self):
    #     self.acceleration.y -= mob_acc

    def move_down(self):
        self.acceleration.y += mob_acc

    def jump(self):
        # TODO:
        # Max jump
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self,
                                       self.game.platforms_group,
                                       False)
        self.rect.x -= 1


        if hits:
            now = pg.time.get_ticks()
            if now - self.last_jump > self.jump_delay:
                self.velocity.y += -abs(MOB_JUMP_POWER)

    def free_move(self):
        # dx = self.game.player.rect.x - self.rect.x
        # dy = self.game.player.rect.y - self.rect.y
        # print("DISTANCE FROM PLAYER:", dy)

        # print(self.game.player.right - self.rect.left)

        # if not dx > self.aggro_range:
        #     self.move_right()
        # elif not dx < self.aggro_range:
        #     self.move_left()

        # print(dx)

        # Aggro range is the square root of all x1 - x2 and
        # y1 - y2 distances less than aggro range

        hits = pg.sprite.groupcollide(self.game.bullets_group,
                                      self.game.mobs_group, False, False)

        if abs(self.dpy) >= 0 and abs(self.dpy) <= self.aggro_range and not hits:
            if abs(self.dpx) >= 0 and abs(self.dpx) <= self.aggro_range and not hits:
                self.chase_x()
            self.chase_y()

        if hits:
            self.chase_x()
        else:
            self.back_forth()

            # if dx >= 0 and not dx > self.aggro_range:
            #     # and not dx > self.aggro_range:
            #     print("HAVE AGGRO")
            #     self.chase_x(dx)

            # elif dx <= 0 and not dx < -abs(self.aggro_range):
            #     print("HAVE AGGRO")
            #     self.chase_x(dx)

            # elif abs(dx) > self.aggro_range:
            #     print("NO AGGRO")

        # last_pdu = abs(self.game.player.rect.y - self.rect.y)
        # if self.game.player.rect.y < self.rect.y:
        #     pdu = abs(self.game.player.rect.y - self.rect.y)
        #     if pdu < last_pdu:
        #         self.jump()
        #         last_pdu = pdu


        # if dy < 0:
        #     self.jump()

        # if dy < self.aggro_range:
        #     self.jump()

    def chase_x(self):
        # print(self.dpx)

        if self.dpx > 0:
            self.move_right()
        if self.dpx < 0:
            self.move_left()

    def chase_y(self):
        # print(abs(self.dpy))
        # TODO
        # Fix mob jump so that they only just when necessary
        # if self.dpy < 0 and self.dpy > - screen_height - 100:
        if abs(self.dpy) < 10:
            self.jump()

    def free_move_jump(self):
        hits = pg.sprite.groupcollide(self.game.bullets_group,
                                      self.game.mobs_group, False, False)

        if abs(self.dpy) >= 0 and abs(self.dpy) <= self.aggro_range and not hits:
            if abs(self.dpx) >= 0 and abs(self.dpx) <= self.aggro_range and not hits:
                self.chase_x()
            self.chase_y()

        if hits:
            self.chase_x()
            self.chase_y()
        else:
            self.back_forth()

    # TODO:
    def back_forth(self):
        # Back and forth left right distance
        # self.movement_range = random.choice([i for i in range(1, 30)])
        # print(s_range = 0
        # self.lr = "l"
        hits = pg.sprite.groupcollide(self.game.bullets_group,
                                      self.game.mobs_group, False, False)

        if not hits:
            if self.cur_range < self.movement_range and self.lr == "l" and not hits:
                if abs(self.distance_edge_left_x) > 0:
                        self.move_left()
                        self.cur_range += 1

                elif self.rect.x > screen_width / 2:
                    self.cur_range = self.movement_range
                    self.lr = "r"
                    self.cur_range = 0

                if self.cur_range >= self.movement_range:

                    self.lr = "r"
                    self.cur_range = 0
                    # print("MOVING TOWARDS", self.lr)

            if self.cur_range < self.movement_range and self.lr == "r" and not hits:
                if abs(self.distance_edge_right_x) > 0:
                    self.move_right()
                    self.cur_range += 1
                elif self.rect.x < screen_width / 2:
                    self.cur_range = self.movement_range
                    self.lr = "l"
                    self.cur_range = 0

                elif self.rect.x < screen_width / 2:
                     self.cur_range = self.movement_range

                if self.cur_range >= self.movement_range:

                    self.lr = "l"
                    self.cur_range = 0
                    # print("MOVING TOWARDS", self.lr)

        elif hits:
            self.chase_x()

        # print("MOVEMENT RANGE:",self.movement_range)
        # print("CURRENT RANGE :",self.cur_range)

        # TODO:
        # Flying mobs

# PlatformPlatformPlatform

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        pg._layer = platform_layer
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(platform_color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game

# TODO:
class Bullet(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pg._layer = bullet_layer
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((9, 9))
        self.image.fill(bullet_color)
        self.rect = self.image.get_rect()

        # For range
        self.lifetime = pg.time.get_ticks()

        # Get mouse position
        self.target = vec(pg.mouse.get_pos())

        # Start at player
        self.position = vec(self.game.player.position)
        self.start_pos = vec(self.game.player.position)
        self.position.y -= 5

        # Distance
        self.distance = self.target.x - self.position.x

        self.start_life = pg.time.get_ticks()

        # x and y distance, also the opposite and adjacent
        # Ratio of x and y distance is also the tangent or
        # angle
        self.dy = self.target.y - self.position.y
        self.dx = self.target.x - self.position.x

        self.angle = 0

        # Normalize vector
        # https://encrypted.google.com/search?hl=en&q=normalizing%20vectors
        self.nize = math.sqrt(self.dx ** 2 + self.dy ** 2)

    def update(self):
        # if BULLET_SHREAD:
        #     self.position.y += (self.dy / self.angle) * bullet_speed)
        #     self.position.x += (self.dx / self.angle) * bullet_speed)

        # elif not BULLET_SHREAD:
        self.position.x += (self.dx / self.nize ) * bullet_speed
        self.position.y += (self.dy / self.nize) * bullet_speed

        now = pg.time.get_ticks()
        if now - self.start_life > bullet_lifetime:
            self.kill()

        self.rect.x = self.position.x
        self.rect.y = self.position.y

        # TODO:
        # Move this here
        # If the bullets hit mobs
        # for m in self.game.mobs_group:
        #     hits = pg.sprite.spritecollide(m,
        #                                    self.game.bullets_group,
        #                                    True,
        #                                    False)
        #     if hits:
        #         m.health -= bullet_damage * self.game.player.level
        #         m.acceleration.x -= self.dx / 10
        #         m.acceleration.y -= self.dy / 10

# TODO:
class HP_Well(pg.sprite.Sprite):
    def __init__(self, game, x=(350+(200/2)), y=(200-30)):
        self.game = game
        pg._layer = platform_layer
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 10))
        self.image.fill(magenta)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        # print("test hp well update")
        hits = pg.sprite.spritecollide(self,
                                       self.game.player_group,
                                       False,
                                       False)
        if hits and self.game.player.cur_hp < 100:
            # print("test hp well collision")
            self.game.player.cur_hp += 1
            self.kill()

        hits = pg.sprite.spritecollide(self,
                                       self.game.mobs_group,
                                       False,
                                       False)
        if hits:
            self.kill()

# TODO:
class Turret(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.game = game
        pg._layer = platform_layer
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(platform_color)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
