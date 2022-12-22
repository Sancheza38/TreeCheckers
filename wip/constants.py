from collections import namedtuple
import pygame as pg
import os
pg.init()
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
UNITS_NUM = 18
RAD = 30
