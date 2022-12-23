import pygame as pg
from typing import Tuple
from dataclasses import dataclass
import constants
@dataclass
class Unit:
    """Unit class"""
    num: int
    player: int
    link: int
    x: float
    y: float
    alive: bool
    king: bool
    radius: float = constants.RAD

    def __post_init__(self):
        """initialize color of unit"""
        if self.player == 0:
            if self.king:
                self.color = constants.LIGHT_CYAN
            else: 
                self.color = constants.DARK_CYAN
        else:
            if self.king: 
                self.color = constants.LIGHT_MAGENTA
            else: 
                self.color = constants.DARK_MAGENTA

    def updatePosition(self,x_y_pair):
        """Updates unit position"""
        self.x,self.y=x_y_pair

    def render(self, screen) -> None:
        """Renders the hexagon on the screen"""
        x,y = self.center
        pg.draw.circle(screen, self.color, (x+1.1,y+1), self.radius)

    @property
    def center(self) -> Tuple[float, float]:
        """Centre of the circle unit"""
        return (self.x,self.y)