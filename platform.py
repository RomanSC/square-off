""" platform.py | Tue, Apr 04, 2017 | Roman S. Collins
"""
import pygame as pg
import random, os

from constants import *

vec = pg.math.Vector2

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg._layer = platform_layer
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(platform_color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
