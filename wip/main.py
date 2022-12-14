# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 13:50:07 2022

@author: richa
"""
import os
import random
from typing import List
from typing import Tuple

import pygame
from hexagon import FlatTopHexagonTile
from hexagon import HexagonTile
from Unit import Unit
import math
pygame.init()



# pylint: disable=no-member
LIGHT_CYAN = (85, 255, 255)
LIGHT_MAGENTA = (255, 85, 255)
DARK_CYAN = (0, 170, 170)
DARK_MAGENTA = (170, 0, 170)
current_player = LIGHT_CYAN
cur_player = 0
nxt_player = 1
next_player = LIGHT_MAGENTA
UNITS_NUM = 18
circle=None


_FONT_PATH = os.path.join("wip","ModernDOS8x8.ttf")
font = pygame.font.Font(_FONT_PATH, 31)
player = font.render("Player 1", False, DARK_CYAN)
nextPlayer = font.render("Player 2", False, DARK_MAGENTA)

def create_hexagon(position, radius=34.64, flat_top=False) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    class_ = FlatTopHexagonTile if flat_top else HexagonTile
    return class_(radius, position, colour=(255, 255, 255))

def get_random_colour(min_=254, max_=255) -> Tuple[int, ...]:
    """Returns a random RGB colour with each component between min_ and max_"""
    return tuple(random.choices(list(range(min_, max_)), k=3))

def init_units(UNITS_NUM=18) -> List[Unit]:
    """Creates a list of unit pieces for the gameboard"""
    i,j,j1,j2,dd,best_dd,best = None
    h=960
    w=1280
    rad=34.64
    border_y = 108
    border_x = 115
    circle = Unit[UNITS_NUM]
    for unit in range(UNITS_NUM/2):
        circle[unit].num=unit
        circle[unit+UNITS_NUM/2].num=unit+UNITS_NUM/2
        def ti_restart():
            circle[unit].y= math.floor((random.randrange(0,4294967295)%960)-(34.64*2))+34.64
            circle[unit+UNITS_NUM/2].y=h-1-circle[unit].y
            j1 = circle[unit].y/(rad*2)
            j2 = circle[unit+UNITS_NUM/2].y/(rad*2)
            circle[unit].y+=border_y

            if not unit:
                circle[unit].x=rad
                if j1&1:
                    ti_restart()
            else:
                circle[unit].x=math.floor((random.randrange(0,4294967295)%((w-rad*2*2)/2))-(34.64*2))+34.64
        
        ti_restart()
        circle[unit+UNITS_NUM/2].x=w-1-circle[unit].x
        if j1&1:
            circle[unit].x+=rad
        if j2&1:
            circle[unit+UNITS_NUM/2].x+=rad
        circle[unit].x+=border_x
        circle[unit+UNITS_NUM/2].x+=border_x


def init_hexagons(num_x=17, num_y=14, flat_top=False) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    # pylint: disable=invalid-name
    #(159,150)
    leftmost_hexagon = create_hexagon(position=(115,108), flat_top=flat_top)
    hexagons = [leftmost_hexagon]
    for x in range(num_y):
        if x:
            # alternate between bottom left and bottom right vertices of hexagon above
            index = 4 if x % 2 == 1 or flat_top else 2
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(leftmost_hexagon)

        # place hexagons to the left of leftmost hexagon, with equal y-values.
        hexagon = leftmost_hexagon
        for i in range(num_x):
            x, y = hexagon.position  # type: ignore
            if flat_top:
                if i % 2 == 1:
                    position = (x + hexagon.radius * 3 / 2, y - hexagon.minimal_radius)
                else:
                    position = (x + hexagon.radius * 3 / 2, y + hexagon.minimal_radius)
            else:
                position = (x + hexagon.minimal_radius * 2, y)
            hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(hexagon)

    return hexagons


def render(screen, hexagons, circle):
    """Renders hexagons on the screen"""
    screen.fill(current_player)
    screen.blit(player,(4,5))

    for hexagon in hexagons:
        hexagon.render(screen)
        hexagon.render_highlight(screen, border_colour=(0, 0, 0))
    circle.render(screen)
    pygame.display.flip()

def render_mouse_down(screen, hexagons, circle, distance):
    """Renders hexagons on the screen"""

    screen.fill(current_player)
    screen.blit(player,(4,5))
    start_position = (circle.x, circle.y)
    current_position = circle.center
    for hexagon in hexagons:
        hexagon.render(screen)
        hexagon.render_highlight(screen, border_colour=(0, 0, 0))

    # draw borders around colliding hexagons and neighbours
    mouse_pos = pygame.mouse.get_pos()
    colliding_hexagons = [
        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
    ]
    for hexagon in colliding_hexagons:
        hexagon.render_highlight(screen, border_colour=(255, 255, 255))
        hexagon.colour=current_player
        if math.dist(start_position, hexagon.centre) < 130 and distance < 130:
            distance+= math.dist(start_position, hexagon.centre)
            circle.center=hexagon.centre
            current_position = circle.center
            circle.render(screen)

        else:
            circle.center=current_position
            circle.render(screen)

    # circle.render(screen)
    pygame.display.flip()
    return distance

def changePlayer():
    global current_player, next_player, player, nextPlayer
    current_player, next_player, player, nextPlayer = next_player, current_player, nextPlayer, player


def main():
    """Main function"""
    distance = 0
    temp=None
    pygame.init()
    mouse_down = False
    screen = pygame.display.set_mode((1280, 960))
    clock = pygame.time.Clock()
    hexagons = init_hexagons(flat_top=False)
    #unit_list = init_units(UNITS_NUM=UNITS_NUM)
    count = 0
    circle = Unit(num=1,center=hexagons[count].centre,x=hexagons[count].centre[0], y=hexagons[count].centre[1], player=1, link=2, color=DARK_MAGENTA, alive=True, radius=30, king=True)
    temp=circle.center
    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                changePlayer()
                if count < 251: count+=1
                else: count=0
                # circle.center = hexagons[count].centre
                distance = 0
                temp = circle.center
                circle.center = temp
                newX, newY = circle.center[0], circle.center[1]
                circle.x=newX
                circle.y=newY

        for hexagon in hexagons:
            hexagon.update()

        if mouse_down == True:
            render_mouse_down(screen, hexagons, circle, distance)
          
        else:
            render(screen, hexagons, circle)

        clock.tick(50)
    pygame.display.quit()


if __name__ == "__main__":
    main()
