""" constants.py | Tue, Apr 04, 2017 | Roman S. Collins
"""
import pygame as pg
import random, os

from os import path

vec = pg.math.Vector2

# Title
title = "Square Off"

# Score file
score_file = "high_scores.txt"

# File IO
self_dir = "./"
texture_dir = "assets/textures/"
mob_texture_dir = "assets/textures/mobs"
logo_dir = "assets/textures/logo"
font_dir = "assets/font"
sounds_dir = "assets/sounds/"

# Fonts
font_name = "guru meditation nbp"

# Difficulty
difficulty_easy = 3
difficulty_medium = 6
difficulty_hard = 8
difficulty_very_hard = 12
difficulty_insane = 20
difficulty = difficulty_medium

# Graphics
screen_width = 960
screen_height = 960
fps = 60

# Player physics
player_gravity = 0.8
player_acc = 0.5
player_fric = -0.12
xp_rate = 0.10

# Mob physics and properties
mob_gravity = 0.7
mob_acc = 0.3
mob_fric = -0.14
mob_spawn_rate = 800
spawn_locations = [(920, 920)]
mobbackforthranges = [i for i in range(200, (screen_width - 50), 20)]

# Bullet physics and properties
bullet_damage = 20
bullet_speed = 10
bullet_lifetime = 1500 # in ms, or thousands of a second
bullet_rate = 70

# Vectors
vec = pg.math.Vector2

# Sprite layers
player_layer = 2
platform_layer = 1
mob_layer = 2
bullet_layer = 1

# Platforms
# platform_list[0] should always be the floor platform
platform_list = [(screen_width - screen_width, screen_height - 40, screen_width + screen_width , 40),
                 (screen_width / 2 - 50, screen_height * 3 / 4, 100, 20),
                 (125, screen_height - 350, 100, 20),
                 (350, 200, 100, 20),
                 (175, 100, 50, 20)]

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
magenta = (255, 0, 255)
cyan = (0, 255, 255)
colors = [white, black, red, green, blue, yellow, magenta, cyan]

# Platform color
platform_color = (29, 20, 19)

# UI colors
bg_color = (90, 35, 35)

# Sprites
bullet_color = cyan
# mob_colors = [[126, 40, 33], [104, 40, 33], [104, 40, 0], [104, 40, 0],
#               [104, 40, 0], [104, 40, 0], [192, 172, 26], [104, 59, 0],
#             [126, 40, 33], [104, 78, 81], [138, 133, 26], [126, 40, 33],
#             [126, 40, 33], [156, 142, 165], [126, 40, 33], [126, 40, 33],
#             [126, 40, 33], [126, 40, 33], [61, 66, 66], [61, 66, 66],
#             [61, 66, 66], [61, 51, 66], [61, 51, 66], [41, 31, 8],
#             [90, 18, 8], [90, 18, 8], [33, 41, 42]]


mob_colors = [[100, 0, 0], [101, 0, 0], [102, 0, 0], [103, 0, 0], [104, 0, 0],
              [105, 0, 0], [106, 0, 0], [107, 0, 0], [108, 0, 0], [109, 0, 0],
              [110, 0, 0], [111, 0, 0], [112, 0, 0], [113, 0, 0], [114, 0, 0],
              [115, 0, 0], [116, 0, 0], [117, 0, 0], [118, 0, 0], [119, 0, 0],
              [120, 0, 0], [121, 0, 0], [122, 0, 0], [123, 0, 0], [124, 0, 0],
              [125, 0, 0], [126, 0, 0], [127, 0, 0], [128, 0, 0], [129, 0, 0],
              [130, 0, 0], [131, 0, 0], [132, 0, 0], [133, 0, 0], [134, 0, 0],
              [135, 0, 0], [136, 0, 0], [137, 0, 0], [138, 0, 0], [139, 0, 0],
              [140, 0, 0], [141, 0, 0], [142, 0, 0], [143, 0, 0], [144, 0, 0],
              [145, 0, 0], [146, 0, 0], [147, 0, 0], [148, 0, 0], [149, 0, 0],
              [150, 0, 0], [151, 0, 0], [152, 0, 0], [153, 0, 0], [154, 0, 0],
              [155, 0, 0], [156, 0, 0], [157, 0, 0], [158, 0, 0], [159, 0, 0],
              [160, 0, 0], [161, 0, 0], [162, 0, 0], [163, 0, 0], [164, 0, 0],
              [165, 0, 0], [166, 0, 0], [167, 0, 0], [168, 0, 0], [169, 0, 0],
              [170, 0, 0], [171, 0, 0], [172, 0, 0], [173, 0, 0], [174, 0, 0],
              [175, 0, 0], [176, 0, 0], [177, 0, 0], [178, 0, 0], [179, 0, 0],
              [180, 0, 0], [181, 0, 0], [182, 0, 0], [183, 0, 0], [184, 0, 0],
              [185, 0, 0], [186, 0, 0], [187, 0, 0], [188, 0, 0], [189, 0, 0],
              [190, 0, 0], [191, 0, 0], [192, 0, 0], [193, 0, 0], [194, 0, 0],
              [195, 0, 0], [196, 0, 0], [197, 0, 0], [198, 0, 0], [199, 0, 0]]

bgimg = pg.image.load(os.path.join(texture_dir, "background.png"))

# Start screen logo
img0 = pg.image.load(os.path.join(logo_dir, "0.png"))
img1 = pg.image.load(os.path.join(logo_dir, "1.png"))
img2 = pg.image.load(os.path.join(logo_dir, "2.png"))
img3 = pg.image.load(os.path.join(logo_dir, "3.png"))
img4 = pg.image.load(os.path.join(logo_dir, "4.png"))
img5 = pg.image.load(os.path.join(logo_dir, "5.png"))
img6 = pg.image.load(os.path.join(logo_dir, "6.png"))
img7 = pg.image.load(os.path.join(logo_dir, "7.png"))
img8 = pg.image.load(os.path.join(logo_dir, "8.png"))
img9 = pg.image.load(os.path.join(logo_dir, "9.png"))
img10 = pg.image.load(os.path.join(logo_dir, "10.png"))
img11 = pg.image.load(os.path.join(logo_dir, "11.png"))
img12 = pg.image.load(os.path.join(logo_dir, "12.png"))
img13 = pg.image.load(os.path.join(logo_dir, "13.png"))
img14 = pg.image.load(os.path.join(logo_dir, "14.png"))
img15 = pg.image.load(os.path.join(logo_dir, "15.png"))
img16 = pg.image.load(os.path.join(logo_dir, "16.png"))
img17 = pg.image.load(os.path.join(logo_dir, "17.png"))
img18 = pg.image.load(os.path.join(logo_dir, "18.png"))
img19 = pg.image.load(os.path.join(logo_dir, "19.png"))
img20 = pg.image.load(os.path.join(logo_dir, "20.png"))
img21 = pg.image.load(os.path.join(logo_dir, "21.png"))
img22 = pg.image.load(os.path.join(logo_dir, "22.png"))
img23 = pg.image.load(os.path.join(logo_dir, "23.png"))
img24 = pg.image.load(os.path.join(logo_dir, "24.png"))
img25 = pg.image.load(os.path.join(logo_dir, "25.png"))
img26 = pg.image.load(os.path.join(logo_dir, "26.png"))
img27 = pg.image.load(os.path.join(logo_dir, "27.png"))
img28 = pg.image.load(os.path.join(logo_dir, "28.png"))
img29 = pg.image.load(os.path.join(logo_dir, "29.png"))
img30 = pg.image.load(os.path.join(logo_dir, "30.png"))
img31 = pg.image.load(os.path.join(logo_dir, "31.png"))
img32 = pg.image.load(os.path.join(logo_dir, "32.png"))
img33 = pg.image.load(os.path.join(logo_dir, "33.png"))
img34 = pg.image.load(os.path.join(logo_dir, "34.png"))
img35 = pg.image.load(os.path.join(logo_dir, "35.png"))

logo_list = [img0, img1, img2, img3, img4,
             img5, img6, img7, img8, img9,
             img10, img11, img12, img13, img14,
             img15, img16, img17, img18, img19,
             img20, img21, img22, img23, img24,
             img25, img26, img27, img28, img29,
             img30, img31, img32, img33, img34,
             img35]

# Mob textures
mob0 = pg.image.load(os.path.join(mob_texture_dir, "mob0.png"))
mob1 = pg.image.load(os.path.join(mob_texture_dir, "mob1.png"))
mob2 = pg.image.load(os.path.join(mob_texture_dir, "mob2.png"))
mob3 = pg.image.load(os.path.join(mob_texture_dir, "mob3.png"))
mob4 = pg.image.load(os.path.join(mob_texture_dir, "mob4.png"))
mob5 = pg.image.load(os.path.join(mob_texture_dir, "mob5.png"))
mob6 = pg.image.load(os.path.join(mob_texture_dir, "mob6.png"))
mob7 = pg.image.load(os.path.join(mob_texture_dir, "mob7.png"))
mob8 = pg.image.load(os.path.join(mob_texture_dir, "mob8.png"))
mob9 = pg.image.load(os.path.join(mob_texture_dir, "mob9.png"))
mob10 = pg.image.load(os.path.join(mob_texture_dir, "mob10.png"))
mob11 = pg.image.load(os.path.join(mob_texture_dir, "mob11.png"))
mob12 = pg.image.load(os.path.join(mob_texture_dir, "mob12.png"))
mob13 = pg.image.load(os.path.join(mob_texture_dir, "mob13.png"))
mob14 = pg.image.load(os.path.join(mob_texture_dir, "mob14.png"))
mob15 = pg.image.load(os.path.join(mob_texture_dir, "mob15.png"))
mob16 = pg.image.load(os.path.join(mob_texture_dir, "mob16.png"))
mob17 = pg.image.load(os.path.join(mob_texture_dir, "mob17.png"))
mob18 = pg.image.load(os.path.join(mob_texture_dir, "mob18.png"))
mob19 = pg.image.load(os.path.join(mob_texture_dir, "mob19.png"))
mob20 = pg.image.load(os.path.join(mob_texture_dir, "mob20.png"))

mob_texture_list = [mob0,
mob1, mob2, mob3, mob4,
mob5, mob6, mob7, mob8,
mob9, mob10, mob11, mob12,
mob13, mob14, mob15, mob16,
mob17, mob18, mob19, mob20,]
