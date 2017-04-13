#!/usr/bin/python3
""" ui.py | Tue, Apr 04, 2017 | Roman S. Collins
"""
import pygame as pg
import random, os

from constants import *

class HP_bar(pg.sprite.Sprite):
    def __init__(self, game, x=0, y=0 ):
        pg.sprite.Sprite.__init__(self)
        self.game = game

        self.high = self.game.player.max_hp * 0.75
        self.mid = self.game.player.max_hp * 0.50
        self.low = self.game.player.max_hp * 0.25

        self.bar_color = green

        self.width = 100
        self.height = 20

        self.image = pg.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.image.fill(self.bar_color)

        self.rect.x = x
        self.rect.y = y

    def update(self):
        # TODO:
        # Fix me, adjust so that health bar is always
        # length 0-100 even if player health is over 100
        if self.game.player.cur_hp > 0:
            self.width = self.game.player.cur_hp * 2

        if self.game.player.cur_hp >= self.high and self.game.player.cur_hp > self.mid:
            self.bar_color = green
        if self.game.player.cur_hp < self.high and self.game.player.cur_hp >= self.mid:
            self.bar_color = yellow
        if self.game.player.cur_hp < self.mid:
            self.bar_color = red

        self.image = pg.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.image.fill(self.bar_color)

        self.rect.x = 20
        self.rect.y = 20

logo_images = ['0.png', '1.png', '2.png', '3.png', '4.png',
               '5.png', '6.png', '7.png', '8.png', '9.png',
               '10.png', '11.png', '12.png', '13.png', '14.png',
               '15.png', '16.png', '17.png', '18.png', '19.png',
               '20.png', '21.png', '22.png', '23.png', '24.png',
               '25.png', '26.png', '27.png', '28.png', '29.png',
               '30.png', '31.png', '32.png', '33.png', '34.png',
               '35.png']
# TODO:
# Display alive time in a class
# class Show_Alive_Time():
#     def __init__(self):
#         pass

# def display_alive_time(game, x=screen_width-20, y=20, size=18, color=white):
#     pass
#     # print(dir(game))
#     time = pg.time.get_ticks() - game.start_time

#     font = pg.font.Font(font_name, size)
#     text_surface = font.render(str(time), True, color)
#     text_rect = text_surface.get_rect()
#     text_rect.x = x
#     text_rect.y = y
#     text_surface.blit(game.screen, text_rect)
