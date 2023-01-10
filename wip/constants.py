from collections import namedtuple
import pygame as pg
import math
import os

# pick size of gameboard
repeat=True
while repeat:
    repeat=False
    try:
        val = int(input("Enter game size between 1 and 9\n"))
        if val<1 or val>9:
            print("invalid input\n")
            repeat=True  
    except:
        print("input must be an integer\n")
        repeat=True

pg.init()

# font
_FONT_PATH = os.path.join("wip","ModernDOS8x8.ttf")
FONT = pg.font.Font(_FONT_PATH, 31)

# colors
LIGHT_CYAN = (85, 255, 255)
LIGHT_MAGENTA = (255, 85, 255)
DARK_CYAN = (0, 170, 170)
DARK_MAGENTA = (170, 0, 170)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)

# players
Player = namedtuple('Player',['color', 'number', 'render'])
PLAYER_ONE = Player(LIGHT_CYAN, 0, FONT.render("Player 1", False, DARK_CYAN))
PLAYER_TWO = Player(LIGHT_MAGENTA, 1, FONT.render("Player 2", False, DARK_MAGENTA))

# game constants
COLUMN_ROW = [(18,16),(20,16),(20,16),(22,18),(26,20),(28,22),(32,24),(36,28),(42,32)]
TOTAL_UNITS = [18, 20, 24, 28, 32, 40, 50, 64, 82]
GAME_OVER = FONT.render("Game Over", False,BLACK)
WIDTH = 1280
HEIGHT = 960
UNITS_NUM = TOTAL_UNITS[val-1]
RAD = (16-val)*2
CIRCUMCIRCLE_RAD = RAD*2/math.sqrt(3)
TILE_SIZE = COLUMN_ROW[val-1]
GAME_BORDER= (int((WIDTH-(RAD*2*TILE_SIZE[0])+RAD)/2),int((HEIGHT-(CIRCUMCIRCLE_RAD*3*(TILE_SIZE[1]/2))-RAD/2)/2))
NUM_ALIVE = [UNITS_NUM/2,UNITS_NUM/2]