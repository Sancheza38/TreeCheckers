import pygame as pg
from typing import Tuple
from dataclasses import dataclass
@dataclass
class Unit:
    """Unit class"""

    num: int
    x: float
    y: float
    player: int
    link: int
    color: tuple
    alive: bool
    radius: float
    king: bool

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