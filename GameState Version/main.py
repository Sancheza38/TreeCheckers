import sys 
import math
import random
import pygame as pg
import constants
from typing import List
from hexagon import HexagonTile
from Unit import Unit


class GameState():
    def __init__(self):
        self.current_player = constants.PLAYER_ONE
        self.next_player = constants.PLAYER_TWO
        self.num_alive = constants.NUM_ALIVE
        self.origin: tuple
        self.tempUnit = None
        self.mouse_down = False
        self.game_over = False
        self.hexagons = self.init_hexagons(flat_top=False)
        self.circleUnits = self.init_game_pieces()

    def create_hexagon(self, position, radius=constants.CIRCUMCIRCLE_RAD) -> HexagonTile:
        """Creates a hexagon tile at the specified position"""
        class_ = HexagonTile
        return class_(radius, position, colour=constants.WHITE)

    def init_game_pieces(self, UNITS_NUM=constants.UNITS_NUM) -> List[Unit]:
        """Creates a list of unit pieces for the gameboard"""
        HALF_UNITS_NUM=int(UNITS_NUM/2)
        right_side = [hexagon.centre for hexagon in self.hexagons]
        left_side = [item for item in reversed(right_side)]

        circle = [[0 for x in range(7)] for x in range(UNITS_NUM)]
        for unit in range(HALF_UNITS_NUM):
            
            circle[unit][0],circle[unit+HALF_UNITS_NUM][0]=unit,unit+HALF_UNITS_NUM

            if not unit:
                pick = random.randint(0,constants.TILE_SIZE[1]-1)*constants.TILE_SIZE[0]
                circle[unit][3],circle[unit][4]= right_side[pick]
                circle[unit+HALF_UNITS_NUM][3],circle[unit+HALF_UNITS_NUM][4]= left_side[pick]

            else:
                ti_restart = True
                while ti_restart:
                    ti_restart=False

                    # index = int(random.randint(0,sys.maxsize)%251)
                    index = random.randint(0,constants.TILE_SIZE[0]*constants.TILE_SIZE[1]-1)
                    circle[unit][3],circle[unit][4]= right_side[index]
                    circle[unit+HALF_UNITS_NUM][3],circle[unit+HALF_UNITS_NUM][4]= left_side[index]

                    if right_side[index][0] > 535:
                        ti_restart=True

            # designate a player to each unit
            circle[unit][1]=0
            circle[unit+HALF_UNITS_NUM][1]=1

            # set .alive=True to each unit
            circle[unit][5]=True
            circle[unit+HALF_UNITS_NUM][5]=True

            # set one unit on each side as king=True, and the rest as king=False
            if not unit:
                circle[unit][6]=True
                circle[unit+HALF_UNITS_NUM][6]=True
            else:
                circle[unit][6]=False
                circle[unit+HALF_UNITS_NUM][6]=False

        # create the links between units of the same side.
        for unit in range(HALF_UNITS_NUM):
            if not circle[unit][6]:
                best_dd=sys.maxsize
                for piece in range(HALF_UNITS_NUM):
                    if unit != piece:
                        dd=pow(circle[unit][3]-circle[piece][3], 2)+pow(circle[unit][4]-circle[piece][4], 2)
                        if (circle[piece][3]<circle[unit][3] or circle[piece][6]) and dd<best_dd:
                            best_dd=dd
                            best=piece
                circle[unit][2]=best
                circle[unit+HALF_UNITS_NUM][2]=best+HALF_UNITS_NUM
            else:
                circle[unit][2]=-1
                circle[unit+HALF_UNITS_NUM][2]=-1
        
        num_alive=[HALF_UNITS_NUM]*2
        
        # create and return a list of class Unit
        result = []
        for unit in range(UNITS_NUM):
            new_circle = Unit(*circle[unit])
            result.append(new_circle)
        
        return result

    def init_hexagons(self, num_x=constants.TILE_SIZE[0]-1, num_y=constants.TILE_SIZE[1], flat_top=False) -> List[HexagonTile]:
        """Creates a hexaogonal tile map of size num_x * num_y"""
        leftmost_hexagon = self.create_hexagon(position=constants.GAME_BORDER)
        hexagons = [leftmost_hexagon]
        for x in range(num_y):
            if x:
                # alternate between bottom left and bottom right vertices of hexagon above
                index = 4 if x % 2 == 1 or flat_top else 2
                position = leftmost_hexagon.vertices[index]
                leftmost_hexagon = self.create_hexagon(position)
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
                hexagon = self.create_hexagon(position)
                hexagons.append(hexagon)

        return hexagons
    
    def render(self, screen):
        """Renders hexagons and units on the screen"""
        screen.fill(self.current_player.color)
        screen.blit(self.current_player.render,(4,5))

        for hexagon in self.hexagons:
            hexagon.render(screen)

        alive = []
        for circle in self.circleUnits:
            if circle.alive:
                circle.render(screen)
                alive.append(circle)

        midpoints = []
        for circle in alive:
            if not circle.king:
                pg.draw.line(screen,constants.BLACK,(circle.center),self.circleUnits[circle.link].center,2)
                mid = ((circle.x+self.circleUnits[circle.link].x+2.2)/2,(circle.y+self.circleUnits[circle.link].y+2)/2)
                midpoints.append(mid)
        
        for point in midpoints:
            pg.draw.circle(screen,constants.BLACK,point,7.0)
        
        if self.num_alive[0]==1 or self.num_alive[1]==1:
            screen.blit(constants.GAME_OVER,(constants.WIDTH/2-70, constants.HEIGHT/2))

        pg.display.flip()

    def render_mouse_down(self, screen):
        """Renders hexagons and selected unit on the screen"""
        start_position=self.origin
        screen.fill(self.current_player.color)
        screen.blit(self.current_player.render,(4,5))
        for hexagon in self.hexagons:
            hexagon.render(screen)

        # draw borders around colliding hexagons and neighbours
        mouse_pos = pg.mouse.get_pos()
        colliding_hexagons = [
            hexagon for hexagon in self.hexagons if hexagon.collide_with_point(mouse_pos)
        ]

        alive = []
        for circle in self.circleUnits:
            if circle.alive:
                circle.render(screen)
                alive.append(circle)
        for hexagon in colliding_hexagons:
            for circle in self.circleUnits:
                if  circle==self.tempUnit and math.dist(start_position, hexagon.centre) < 145:
                    # distance = math.dist(start_position, hexagon.centre)
                    # print(distance)
                    circle.updatePosition(hexagon.centre)
                    circle.render(screen)

        midpoints = []
        for circle in alive:
            if not circle.king:
                pg.draw.line(screen,constants.BLACK,(circle.center),self.circleUnits[circle.link].center,2)
                mid = ((circle.x+self.circleUnits[circle.link].x+2.2)/2,(circle.y+self.circleUnits[circle.link].y+2)/2)
                midpoints.append(mid)
        
        for point in midpoints:
            pg.draw.circle(screen,constants.BLACK,point,7.0)
        
        pg.draw.line(screen, constants.RED, (self.origin[0]-10,self.origin[1]+10), (self.origin[0]+10,self.origin[1]-10),2)
        pg.draw.line(screen, constants.RED, (self.origin[0]-10,self.origin[1]-10), (self.origin[0]+10,self.origin[1]+10),2)
        pg.draw.line(screen, constants.RED, self.origin, (self.tempUnit.center[0],self.tempUnit.center[1]),2)

        pg.display.flip()

    def UnitFind(self):
        """finds the best suited allied unit to select, based on mouse position when pressed down"""
        best_dd=sys.maxsize
        mouse_pos = pg.mouse.get_pos()
        for circle in self.circleUnits:
            if circle.player==self.current_player.number and circle.alive:
                dd=pow(circle.x-mouse_pos[0], 2)+pow(circle.y-mouse_pos[1], 2)
                if dd<best_dd:
                    best_dd=dd
                    result=circle
        return result

    def changePlayer(self):
        """finalize current turn action and switch players"""
        self.current_player, self.next_player = self.next_player, self.current_player

    def kill_check(self):
        found:bool

        def verify_links():
            found=False
            for unit in self.circleUnits:
                if unit.alive and unit.player!=self.tempUnit.player and not unit.king and not self.circleUnits[unit.link].alive:
                    found=True
                    unit.alive=False
                    self.num_alive[self.tempUnit.player] -= 1
            return found

        for circle in self.circleUnits:
            if circle.player!=self.tempUnit.player and circle.alive and not circle.king:
                x2=int(circle.x+self.circleUnits[circle.link].x)>>1
                y2=int(circle.y+self.circleUnits[circle.link].y)>>1
                dd=pow(x2-self.tempUnit.x,2)+pow(y2-self.tempUnit.y,2)

                if dd<=(constants.RAD+2)*(constants.RAD+2):
                    circle.alive=False
                    self.num_alive[self.tempUnit.player] -= 1
                
                found = verify_links()

                while found:
                    found = verify_links()


def main():
    """Main function"""
    game_state = GameState()

    mouse_down = False
    game_over = False
    screen = pg.display.set_mode((constants.WIDTH, constants.HEIGHT))
    clock = pg.time.Clock()
    
    terminated = False
    while not terminated:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminated = True
            elif game_state.num_alive[0]==1 or game_state.num_alive[1]==1:
                game_over = True

            elif not game_state.tempUnit and event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                game_state.tempUnit = game_state.UnitFind()
                game_state.origin = game_state.tempUnit.center
                mouse_down = True

            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                mouse_down=False
                game_state.kill_check()
                game_state.changePlayer()
                game_state.origin=None
                game_state.tempUnit=None

        if not game_over and game_state.tempUnit!=None and mouse_down:
            game_state.render_mouse_down(screen)
          
        else:
            game_state.render(screen)

        clock.tick(50)
    pg.display.quit()


if __name__ == "__main__":
    main()