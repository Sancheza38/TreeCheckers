# -*- coding: utf-8 -*-

import os
import sys 
import math
import random
import pygame as pg
import constants
from typing import List
from hexagon import HexagonTile
from unit import Unit

pg.init()

current_player = constants.PLAYER_ONE
next_player = constants.PLAYER_TWO

def create_hexagon(position, radius=34.64) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    class_ = HexagonTile
    return class_(radius, position, colour=constants.WHITE)

def init_units(hexagons, UNITS_NUM=constants.UNITS_NUM) -> List[Unit]:
    """Creates a list of unit pieces for the gameboard"""
    HALF_UNITS_NUM=int(UNITS_NUM/2)
    right_side = [hexagon.centre for hexagon in hexagons]
    left_side = [item for item in reversed(right_side)]

    circle = [[0 for x in range(7)] for x in range(UNITS_NUM)]
    for unit in range(HALF_UNITS_NUM):
        ti_restart = True

        circle[unit][0],circle[unit+HALF_UNITS_NUM][0]=unit,unit+HALF_UNITS_NUM
        while ti_restart:
            
            ti_restart=False
            index = random.randint(0,251)
            circle[unit][3],circle[unit][4]= right_side[index]
            circle[unit+HALF_UNITS_NUM][3],circle[unit+HALF_UNITS_NUM][4]= left_side[index]

            if not unit and right_side[index][0] > 115:
                ti_restart=True
            elif right_side[index][0] > 535:
                ti_restart=True

        circle[unit][1]=0
        circle[unit+HALF_UNITS_NUM][1]=1

        circle[unit][5]=True
        circle[unit+HALF_UNITS_NUM][5]=True

        if not unit:
            circle[unit][6]=True
            circle[unit+HALF_UNITS_NUM][6]=True
        else:
            circle[unit][6]=False
            circle[unit+HALF_UNITS_NUM][6]=False

    for unit in range(HALF_UNITS_NUM):
        if circle[unit][6]==True:
            circle[unit][2]=unit
            circle[unit+HALF_UNITS_NUM][2]=unit+HALF_UNITS_NUM
        else:
            best_dd=sys.maxsize
            for piece in range(HALF_UNITS_NUM):
                if circle[unit][0]!=circle[piece][0]:
                    dd=pow(circle[unit][3]-circle[piece][3], 2)+pow(circle[unit][4]-circle[piece][4], 2)
                    if circle[piece][3]<circle[unit][3] or circle[piece][6] and dd<best_dd:
                        best_dd=dd
                        best=piece
            circle[unit][2]=best
            circle[unit+HALF_UNITS_NUM][2]=best+HALF_UNITS_NUM
    
    num_alive=[HALF_UNITS_NUM]*2
    
    result = []
    for unit in range(UNITS_NUM):
        new_circle = Unit(*circle[unit])
        result.append(new_circle)
    
    return result

def init_hexagons(num_x=17, num_y=14, flat_top=False) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    # pylint: disable=invalid-name
    #(115,108)
    leftmost_hexagon = create_hexagon(position=(115,108))
    hexagons = [leftmost_hexagon]
    for x in range(num_y):
        if x:
            # alternate between bottom left and bottom right vertices of hexagon above
            index = 4 if x % 2 == 1 or flat_top else 2
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position)
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
            hexagon = create_hexagon(position)
            hexagons.append(hexagon)

    return hexagons

def render(screen, hexagons, circleUnits):
    """Renders hexagons and units on the screen"""
    screen.fill(current_player.color)
    screen.blit(current_player.render,(4,5))
    temp=None
    for hexagon in hexagons:
        hexagon.render(screen)
    for circle in circleUnits:
        for circle2 in circleUnits:
            if circle2.link == circle.num:
                temp = circle2
        pg.draw.line(screen,(0,0,0),(circle.center),(temp.center),2)
        circle.render(screen)
    for circle in circleUnits:

        for circle2 in circleUnits:
            if not circle2.king and circle2.link == circle.num:
                temp = circle2
        pg.draw.line(screen,(0,0,0),(circle.center),(temp.center),2)
    pg.display.flip()

def render_mouse_down(screen, hexagons, circleUnits, tempUnit, distance, origin):
    """Renders hexagons and selected unit on the screen"""
    start_position,current_position=list(range(constants.UNITS_NUM)),list(range(constants.UNITS_NUM))
    screen.fill(current_player.color)
    screen.blit(current_player.render,(4,5))
    start_position = origin
    for circle in circleUnits:
        current_position[circle.num] = circle.center
    for hexagon in hexagons:
        hexagon.render(screen)

    # draw borders around colliding hexagons and neighbours
    mouse_pos = pg.mouse.get_pos()
    colliding_hexagons = [
        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
    ]
    for hexagon in colliding_hexagons:
        for circle in circleUnits:
            if  circle==tempUnit and distance < 120 and math.dist(start_position, hexagon.centre) < 120:
                distance+= math.dist(start_position, hexagon.centre)
                circle.updatePosition(hexagon.centre)
                current_position[circle.num] = circle.center
                
            else: circle.updatePosition(current_position[circle.num])
            circle.render(screen)

    for circle in circleUnits: circle.render(screen)
    for circle in circleUnits:
        for circle2 in circleUnits:
            if circle2.link == circle.num:
                temp = circle2
        pg.draw.line(screen,(0,0,0),(circle.center),(temp.center),2)
    
    pg.draw.line(screen, constants.RED, (origin[0]-10,origin[1]+10), (origin[0]+10,origin[1]-10),2)
    pg.draw.line(screen, constants.RED, (origin[0]-10,origin[1]-10), (origin[0]+10,origin[1]+10),2)
    pg.draw.line(screen, constants.RED, origin, (tempUnit.center[0],tempUnit.center[1]),2)

    pg.display.flip()
    return

def UnitFind(circleUnits):
    """finds the best suited allied unit to select, based on mouse position when pressed down"""
    best_dd=sys.maxsize
    mouse_pos = pg.mouse.get_pos()
    for circle in circleUnits:
        if circle.player==current_player.number and circle.alive:
            dd=pow(circle.x-mouse_pos[0], 2)+pow(circle.y-mouse_pos[1], 2)
            if dd<best_dd:
                best_dd=dd
                result=circle
    return result

def changePlayer(tempUnit):
    """finalize current turn action and switch players"""
    global current_player, next_player
    tempUnit.x,tempUnit.y = tempUnit.center
    current_player, next_player = next_player, current_player

def main():
    """Main function"""
    origin: tuple
    distance = 0
    tempUnit = None
    mouse_down = False
    show_start=False
    screen = pg.display.set_mode((1280, 960))
    clock = pg.time.Clock()
    hexagons = init_hexagons(flat_top=False)
    circleUnits = init_units(hexagons)

    terminated = False
    while not terminated:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminated = True

            elif not tempUnit and event.type == pg.MOUSEBUTTONDOWN:
                tempUnit=UnitFind(circleUnits)
                origin = tempUnit.center
                mouse_down = True
                show_start=True

            elif event.type == pg.MOUSEBUTTONUP:
                mouse_down=False
                distance=0
                show_start=False
                changePlayer(tempUnit)
                origin=None
                tempUnit=None

        if tempUnit!=None and mouse_down:
            render_mouse_down(screen, hexagons, circleUnits, tempUnit, distance, origin)
          
        else:
            render(screen, hexagons, circleUnits)

        clock.tick(50)
    pg.display.quit()


if __name__ == "__main__":
    main()
