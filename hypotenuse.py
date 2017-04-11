import matplotlib
import pygame as pg

player_position = (380, 380)
mouse_position = (960, 0)

distance = (mouse_position[0] - player_position[0])

time = 960

for x in range(player_position[0], distance):
    height = time - x
    width = x
    print(width, height)
