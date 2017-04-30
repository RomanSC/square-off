#!/usr/bin/python3
""" main.py | Tue, Apr 04, 2017 | Roman S. Collins
"""
import pygame as pg
import random, os

import time

from constants import *
from sprites import *
from ui import *

vec = pg.math.Vector2

import math

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption(title)

        self.clock = pg.time.Clock()

        self.load_data()

        self.font_name = pg.font.match_font(font_name)

        self.running = True
        self.playing = False

    def load_data(self):
            # JFC this should not be that complicated
            # https://stackoverflow.com/questions/38514177/can-you-read-first-line-from-file-with-openfname-a
        with open(score_file, 'a+') as f: # Read writeable, start at the end
            f.seek(0) # Go to the first line
            self.score_file_lines = f.readlines() # Read in scores

            f.seek(0, 2) # Go back to the end
            f.close()

        thesplit = []
        for x in self.score_file_lines:
            thesplit.append(x.split(":"))

        self.high_score = 0
        self.high_scores = []
        for i in range(1, len(thesplit)):
            # print(thesplit[i])
            if int(thesplit[i][1]) >= self.high_score:
                # print(True)
                # print(thesplit[i][0], thesplit[i][1])
                self.high_score = int(thesplit[i][1])
                self.best_player = thesplit[i][0]

            # print(self.best_player, self.high_score)

    def write_data(self):
        with open(score_file, 'a+') as f: # Read writeable, start at the end
            f.seek(0) # Go to the first line
            self.score_file_lines = f.readlines() # Read in scores

            # f.seek(0)
            # print(f.readline())
            # f.seek(0)

            # print("old:", self.score_file_lines)
            if '# High Scores: DO NOT EDIT\n' == self.score_file_lines[0]:
                hs_header = self.score_file_lines.pop(0)
                #self.score_file_lines.insert(0, self.record_score_string)
                self.score_file_lines.append(self.record_score_string)
                self.score_file_lines.insert(0, hs_header)
                # print("new:", self.score_file_lines)
            elif '# High Scores: DO NOT EDIT\n' not in self.score_file_lines:
                print("High score file corrupted")
                return

        with open(score_file, 'a+') as f: # Read writeable, start at the end
            f.seek(0) # Go to the first line
            self.score_file_lines = f.readlines() # Read in scores

            f.seek(0)
            # print(f.readline())
            f.seek(0)
            for x in self.record_score_string:
                f.write(x)
            f.close()

    # Start a new game
    def new(self):
        self.clock.tick(fps)
        game = self

        # Sprite groups
        self.all_sprites_group = pg.sprite.LayeredUpdates()
        self.player_group = pg.sprite.Group()
        self.mobs_group = pg.sprite.Group()
        self.platforms_group = pg.sprite.Group()
        self.floor_group = pg.sprite.Group()
        self.ui_group = pg.sprite.Group()
        self.bullets_group = pg.sprite.Group()
        self.hp_wells_group = pg.sprite.Group()

        # Individual sprites
        self.player = Player(game)
        self.all_sprites_group.add(self.player)
        self.player_group.add(self.player)

        # Platforms
        floor = platform_list[0]
        self.floor = Platform(self, floor[0], floor[1], floor[2], floor[3])
        self.floor_group.add(self.floor)
        self.platforms_group.add(self.floor)
        self.all_sprites_group.add(self.floor)

        for i in range(1, len(platform_list)-1):
            p = Platform(self, platform_list[i][0], platform_list[i][1], platform_list[i][2], platform_list[i][3])
            self.platforms_group.add(p)
            self.all_sprites_group.add(p)


        # Mobs
        # for m in range(int(self.player.level * difficulty)):
        for m in range(20):
            self.last_spawn = pg.time.get_ticks()
            spawn_pos = random.choice(spawn_locations)
            m = Mob(self, spawn_pos)
            self.mobs_group.add(m)
            self.all_sprites_group.add(m)

        hp_bar = HP_bar(game)
        self.ui_group.add(hp_bar)
        self.all_sprites_group.add(hp_bar)

        self.start_time = pg.time.get_ticks()

        # Last time player shot
        self.last_shot = 0

        # Run the game
        self.run()

    # Game loop
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(fps) / 1000.0

            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:

                if self.playing:
                    self.playing = False
                self.running = False

    # Update
    def update(self):
            # if self.player.cur_hp < 100:
            #     self.player.cur_hp += 100

            self.all_sprites_group.update()

            if self.player.velocity.y > 0:
                # TODO:
                # Optimize collision checking to only check on screen sprites
                # https://youtu.be/OmlQ0XCvIn0?list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&t=339
                # If player hits a platform - only if falling
                hits = pg.sprite.spritecollide(self.player, self.platforms_group, False)

                if hits:
                    self.player.position.y = hits[0].rect.top
                    self.player.velocity.y = 0

            # So mobs don't fall through floor
            for m in self.mobs_group:
                if m.velocity.y > 0:
                    hits = pg.sprite.spritecollide(m, self.platforms_group, False)
                    if hits:
                        m.position.y = hits[0].rect.top
                        m.velocity.y = 0

            # Enemy damage to the player if they collide
            for m in self.mobs_group:
                hits = pg.sprite.spritecollide(self.player, self.mobs_group, False)
                if hits:
                    damage = random.choice(PLAYER_DEFENSE) \
                    - m.attack_damage

                    if damage < 0:
                        self.player.cur_hp -= abs(damage)

            # # Scroll up
            # if self.player.rect.top <= screen_height / 8:
            #     self.player.position.y += abs(self.player.velocity.y)
            #     for mob in self.mobs_group:
            #         mob.rect.y -= abs(self.player.velocity.y)

            #     for plat in self.platforms_group:
            #         plat.rect.y += abs(self.player.velocity.y)

            # # Scroll down, but not past 1/16 of the screen
            # # so that bottom platforms still look nice
            # if self.player.rect.bottom >= screen_height - screen_height / 26:
            #     self.player.position.y -= abs(self.player.velocity.y)
            #     for mob in self.mobs_group:
            #         mob.rect.y -= abs(self.player.velocity.y)

            #     for plat in self.platforms_group:
            #         plat.rect.y -= abs(self.player.velocity.y)


                # Death condition
            if self.player.lives <= 0:
                if self.alive_time > int(self.high_score):
                    self.high_score = "{0:.0f}".format(self.alive_time / 1000)
                    self.record_score_string = "{}:{}:\n".format(self.player, self.high_score)
                    self.write_data()

                self.draw_text("REKT!",
                               screen_width / 2, screen_height / 2,
                               align="right",
                               size=32)
                self.player.kill()

                pg.display.flip()

                time.sleep(1)

                self.playing = False

            # Time survived
            if self.player.lives > 0:
                self.alive_time = pg.time.get_ticks() - self.start_time

            # | Keep respawning mobs when they die

            # print(int(self.player.level) * difficulty)

            # if len(self.mobs_group) < int(self.player.level * difficulty):
            #     now = pg.time.get_ticks()
            #     if now - self.last_spawn > mob_spawn_rate:
		    # # TODO:
		    # # Maximum spawn count
            #         for m in range(int(self.player.level * difficulty)):
            #             self.last_spawn = now
            #             # x_location = random.randrange(0, screen_width)
            #             spawn_pos = random.choice(spawn_locations)
            #             m = Mob(self, spawn_pos)
            #             self.mobs_group.add(m)
            #             self.all_sprites_group.add(m)
            if len(self.mobs_group) < MOB_COUNT:
                # if now - self.last_spawn > mob_spawn_rate:
                for m in range(MOB_COUNT):
                    # x_location = random.randrange(0, screen_width)
                    spawn_pos = random.choice(spawn_locations)
                    m = Mob(self, spawn_pos)
                    self.mobs_group.add(m)
                    self.all_sprites_group.add(m)

                # self.last_spawn = now

            if (self.player.kills % 10) == 0 and self.player.kills != 0:
                print("test")
                hp_well = HP_Well(self)
                self.hp_wells_group.add(hp_well)
                self.all_sprites_group.add(hp_well)

    # Text drawing functions
    def draw_text(self, text, x, y, align="left", size=18, color=white):
        # self.font_name = pg.font.Font(os.path.join(font_dir,
        #                                            "pixelated-font.ttf"), 16)
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, False, color)
        text_rect = text_surface.get_rect()
        text_rect.x, text_rect.y = x, y

        if align == "center":
            text_rect.center = (x, y)
            text_rect.y = y
        if align == "right":
            text_rect.right = x
            text_rect.y = y

        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(bg_color) # In case background image not blit
        self.fill_background()
        self.all_sprites_group.draw(self.screen)

        # Text for kills and alive time
        self.draw_text("Time Survived: {0:.2f}".format(self.alive_time / 1000),
                       screen_width / 2, 20,
                       align="center",
                       size=24)

        self.draw_text("Kills: " + str(self.player.kills),
                       screen_width - 20, 20,
                       align="right",
                       size=24)

        pg.display.flip()

    # Pause until key or click
    def wait_for_key(self, mouse_too=False):
        wait = True
        while wait:
            self.clock.tick(25)
            self.load_logo()

            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    wait = False
                    self.running = False

                if event.type == pg.KEYUP:
                    wait = False

                if mouse_too and event.type == pg.MOUSEBUTTONDOWN:
                    wait = False


    # RGB start screen logo
    def load_logo(self):
        # Endless loop for indexing over the images
        if self.which_img >= 35:
            self.which_img = -1
        self.which_img += 1

        img = logo_list[self.which_img]
        img_rect = img.get_rect()
        img_rect.center = (self.img_pos)
        self.screen.blit(img, img_rect)

    def start_screen(self):
        self.fill_background()

        self.which_img = -1
        self.img_pos = (screen_width/2, 180)

        self.draw_text("Highscore:",
                       screen_width/2,
                       screen_height / 2,
                       align="center",
                       size=32,
                       color=yellow)

        self.draw_text(self.best_player,
                       screen_width/2,
                       (screen_height / 2) + 44,
                       align="center",
                       size=32, color=yellow)

        self.draw_text(str(self.high_score) + " points",
                       screen_width/2,
                       (screen_height / 2) + 84,
                       align="center",
                       size=32, color=yellow)

        self.draw_text("Press any key or click to start",
                       screen_width/2, screen_height - screen_height / 4 + 30,
                       align="center", size=30)

        for img in logo_list:
            img = img.convert()

        pg.display.flip()
        self.wait_for_key(mouse_too=True)

    def fill_background(self):
        # Background
        self.screen.fill(bg_color) # Just in case
        bgimg = pg.image.load(os.path.join(texture_dir, "background.png")).convert()
        self.bgimg_pos = (screen_width/2, screen_height/2)
        self.bgrect = bgimg.get_rect()
        self.bgrect.center = (self.bgimg_pos)
        self.screen.blit(bgimg, self.bgrect)

g = Game()
g.start_screen()

while g.running:
    g.new()

    # TODO:
    # Game over

pg.quit()
