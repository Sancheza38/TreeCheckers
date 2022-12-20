# -*- coding: utf-8 -*-

import os
import sys 
import math
import random
import pygame
from typing import List
from typing import Tuple

from hexagon import FlatTopHexagonTile
from hexagon import HexagonTile
from unit import Unit

pygame.init()

_FONT_PATH = os.path.join("wip","ModernDOS8x8.ttf")
font = pygame.font.Font(_FONT_PATH, 31)

# pylint: disable=no-member
LIGHT_CYAN = (85, 255, 255)
LIGHT_MAGENTA = (255, 85, 255)
DARK_CYAN = (0, 170, 170)
DARK_MAGENTA = (170, 0, 170)
current_player = (LIGHT_CYAN, 0, font.render("Player 1", False, DARK_CYAN))
next_player = (LIGHT_MAGENTA, 1, font.render("Player 2", False, DARK_MAGENTA))
UNITS_NUM = 18
num_alive:list
circle = None
count = 0
#12 6 13 11 13 8 0 4 12
#0 3 5 14 4 9 6 4 1 
def create_hexagon(position, radius=34.64, flat_top=False) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    class_ = FlatTopHexagonTile if flat_top else HexagonTile
    return class_(radius, position, colour=(255, 255, 255))

def init_units_test(UNITS_NUM=18) -> List[Unit]:
    """Creates a list of unit pieces for the gameboard"""
    HALF_UNITS_NUM=int(UNITS_NUM/2)
    h=960
    w=1280
    rad=30 #34.64
    cols=18#int((w-8-rad)/(2*rad))&~1-1
    border_x =(w+rad-cols*2*rad)/2
    rows=14#int(h/(2*rad))&~1
    border_y = 108#(h-rows*2*rad)/2

    circle = [[0 for x in range(10)] for x in range(UNITS_NUM)]
    for unit in range(HALF_UNITS_NUM):
        ti_restart = True
        circle[unit][0]=unit
        circle[unit+HALF_UNITS_NUM][0]=unit+HALF_UNITS_NUM
        while ti_restart:
            ti_restart=False
            num = random.randint(0,4294967295)%h
            circle[unit][3]= num-(num%(rad*2))+rad
            circle[unit+HALF_UNITS_NUM][3]=h-1-circle[unit][3]
            j1 = int(circle[unit][3]/(rad*2))
            j2 = int(circle[unit+HALF_UNITS_NUM][3]/(rad*2))
            circle[unit][3]+=border_y
            
            if not unit:
                circle[unit][2]=rad
                if j1&1:
                    ti_restart=True
            else:
                num = random.randint(0,4294967295)%(w-rad*2*2)/2
                circle[unit][2]= num-num%(rad*2)#math.floor((random.randrange(0,4294967295)%((w-rad*2*2)/2))-(rad*2))+rad
        circle[unit+HALF_UNITS_NUM][2]=w-1-int(circle[unit][2])

        if j1&1:
            circle[unit][2]+=rad
        if j2&1:
            circle[unit+HALF_UNITS_NUM][2]+=rad
        circle[unit][2]+=border_x
        circle[unit+HALF_UNITS_NUM][2]-=border_x

        def S2Circle(x,y):
            
            tempY=int((y-border_y)/(rad*2))
            if tempY&1:
                tempX=(x-rad-border_x)/(rad*2)
            else:
                tempX=(x-border_x)/(rad*2)
            return tempX,tempY

        def Circle2S(x,y):
            
            print(x,y)
            tempY=y*rad*2+rad+border_y
            tempX=x*rad*2+rad+border_x
            if int(tempY)&1:
                tempX+=rad
            return tempX,tempY

        circle[unit][2],circle[unit][3]=S2Circle(circle[unit][2],circle[unit][3])
        circle[unit][2],circle[unit][3]=Circle2S(circle[unit][2],circle[unit][3])

        circle[unit+HALF_UNITS_NUM][2],circle[unit+HALF_UNITS_NUM][3]=S2Circle(circle[unit+HALF_UNITS_NUM][2],circle[unit+HALF_UNITS_NUM][3])
        circle[unit+HALF_UNITS_NUM][2],circle[unit+HALF_UNITS_NUM][3]=Circle2S(circle[unit+HALF_UNITS_NUM][2],circle[unit+HALF_UNITS_NUM][3])

        circle[unit][4]=0
        circle[unit+HALF_UNITS_NUM][4]=1

        circle[unit][7]=True
        circle[unit+HALF_UNITS_NUM][7]=True

        if not unit:
            circle[unit][6]=LIGHT_CYAN
            circle[unit+HALF_UNITS_NUM][6]=LIGHT_MAGENTA
            circle[unit][9]=True
            circle[unit+HALF_UNITS_NUM][9]=True
        else:
            circle[unit][6]=DARK_CYAN
            circle[unit+HALF_UNITS_NUM][6]=DARK_MAGENTA
            circle[unit][9]=False
            circle[unit+HALF_UNITS_NUM][9]=False

    for unit in range(HALF_UNITS_NUM):
        if circle[unit][9]==True:
            circle[unit][5]=unit
            circle[unit+HALF_UNITS_NUM][5]=unit+HALF_UNITS_NUM
        else:
            best_dd=sys.maxsize
            for piece in range(HALF_UNITS_NUM):
                if circle[unit][0]!=circle[piece][0]:
                    dd=pow(circle[unit][2]-circle[piece][2], 2)+pow(circle[unit][3]-circle[piece][3], 2)
                    if circle[piece][2]<circle[unit][2] or circle[piece][9] and dd<best_dd:
                        best_dd=dd
                        best=piece
            circle[unit][5]=best
            circle[unit+HALF_UNITS_NUM][5]=best+HALF_UNITS_NUM
    num_alive=[HALF_UNITS_NUM]*2
    new_circle = create_circle(circle[0])
    print(new_circle)
    result = [new_circle]

    for unit in range(1,UNITS_NUM):
        new_circle = create_circle(circle[unit])
        print(new_circle)
        result.append(new_circle)
    
    return result

def create_circle(circle:list) -> Unit:
    return Unit(circle[0],(circle[2],circle[3]),circle[2],circle[3],circle[4],circle[5],circle[6],circle[7], 30.0,circle[9])

        

def init_units(UNITS_NUM, hexagons) -> List[Unit]:
    """Creates a list of unit pieces for the gameboard"""
    circle1 = Unit(num=1,center=hexagons[1].centre, x=hexagons[1].centre[0], y=hexagons[1].centre[1], player=1, link=2, color=DARK_MAGENTA, alive=True, radius=30, king=True)
    circle2 = Unit(num=2,center=hexagons[2].centre, x=hexagons[2].centre[0], y=hexagons[2].centre[1], player=1, link=1, color=DARK_MAGENTA, alive=True, radius=30, king=False)
    circle3 = Unit(num=3,center=hexagons[3].centre, x=hexagons[3].centre[0], y=hexagons[3].centre[1], player=0, link=4, color=DARK_CYAN, alive=True, radius=30, king=True)
    circle4 = Unit(num=4,center=hexagons[4].centre, x=hexagons[4].centre[0], y=hexagons[4].centre[1], player=0, link=3, color=DARK_CYAN, alive=True, radius=30, king=False)
    circleUnits = [circle1, circle2, circle3, circle4]
    return circleUnits

def init_hexagons(num_x=17, num_y=14, flat_top=False) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    # pylint: disable=invalid-name
    #(115,108)
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

def render(screen, hexagons, circleUnits):
    """Renders hexagons and units on the screen"""
    screen.fill(current_player[0])
    screen.blit(current_player[2],(4,5))
    temp=None
    for hexagon in hexagons:
        hexagon.render(screen)
        hexagon.render_highlight(screen, border_colour=(0, 0, 0))
    for circle in circleUnits:
        for circle2 in circleUnits:
            if circle2.link == circle.num:
                temp = circle2
        pygame.draw.line(screen,(0,0,0),(circle.center),(temp.center),2)
        circle.render(screen)
    for circle in circleUnits:

        for circle2 in circleUnits:
            if not circle2.king and circle2.link == circle.num:
                temp = circle2
        pygame.draw.line(screen,(0,0,0),(circle.center),(temp.center),2)
    pygame.display.flip()

def render_mouse_down(screen, hexagons, circleUnits, tempUnit, distance, origin):
    """Renders hexagons and selected unit on the screen"""
    start_position=list(range(UNITS_NUM))
    current_position=list(range(UNITS_NUM))
    screen.fill(current_player[0])
    screen.blit(current_player[2],(4,5))
    for circle in circleUnits:
        start_position[circle.num] = (circle.x, circle.y)
        current_position[circle.num] = circle.center
    for hexagon in hexagons:
        hexagon.render(screen)
        hexagon.render_highlight(screen, border_colour=(0, 0, 0))

    # draw borders around colliding hexagons and neighbours
    mouse_pos = pygame.mouse.get_pos()
    colliding_hexagons = [
        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
    ]
    for hexagon in colliding_hexagons:
        for circle in circleUnits:
            if  circle==tempUnit and distance < 180 and math.dist(start_position[circle.num], hexagon.centre) < 180:
                distance+= math.dist(start_position[circle.num], hexagon.centre)
                circle.center=hexagon.centre
                current_position[circle.num] = circle.center
                
            else: circle.center=current_position[circle.num]
            circle.render(screen)

    for circle in circleUnits: circle.render(screen)
    for circle in circleUnits:
        for circle2 in circleUnits:
            if circle2.link == circle.num:
                temp = circle2
        pygame.draw.line(screen,(0,0,0),(circle.center),(temp.center),2)
    
    pygame.draw.line(screen,(255,0,0), (origin[0]-10,origin[1]+10), (origin[0]+10,origin[1]-10),2)
    pygame.draw.line(screen,(255,0,0), (origin[0]-10,origin[1]-10), (origin[0]+10,origin[1]+10),2)
    pygame.draw.line(screen,(255,0,0), (origin[0],origin[1]), (tempUnit.center[0],tempUnit.center[1]),2)

    pygame.display.flip()
    return

def UnitFind(circleUnits):
    """finds the best suited allied unit to select, based on mouse position when pressed down"""
    dd=None
    best_dd=sys.maxsize
    result=None
    mouse_pos = pygame.mouse.get_pos()
    for circle in circleUnits:
        if circle.player==current_player[1] and circle.alive:
            dd=pow(circle.x-mouse_pos[0], 2)+pow(circle.y-mouse_pos[1], 2)
            if dd<best_dd:
                best_dd=dd
                result=circle
    return result

def changePlayer(tempUnit):
    """finalize current turn action and switch players"""
    global current_player, next_player
    tempUnit.x,tempUnit.y = tempUnit.center[0],tempUnit.center[1]
    current_player, next_player = next_player, current_player
    return tempUnit

def main():
    """Main function"""
    origin=None
    distance = 0
    tempUnit = None
    pygame.init()
    mouse_down = False
    show_start=False
    screen = pygame.display.set_mode((1280, 960))
    clock = pygame.time.Clock()
    hexagons = init_hexagons(flat_top=False)
    print(hexagons[251].centre)
    #unit_list = init_units(UNITS_NUM=UNITS_NUM)
    circleUnits = init_units_test(18)

    # circleUnits = init_units(18, hexagons)

    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True

            elif not tempUnit and event.type == pygame.MOUSEBUTTONDOWN:
                tempUnit=UnitFind(circleUnits)
                origin = tempUnit.center
                mouse_down = True
                show_start=True

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down=False
                distance=0
                show_start=False
                changePlayer(tempUnit)
                origin=None
                tempUnit=None

        for hexagon in hexagons:
            hexagon.update()

        if tempUnit!=None and mouse_down:
            count = render_mouse_down(screen, hexagons, circleUnits, tempUnit, distance, origin)
          
        else:
            render(screen, hexagons, circleUnits)

        clock.tick(50)
    pygame.display.quit()


if __name__ == "__main__":
    main()
