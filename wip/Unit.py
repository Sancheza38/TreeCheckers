import pygame as pg
from dataclasses import dataclass

@dataclass
class Unit:
    num: int
    center: tuple
    x: float
    y: float
    player: int
    link: int
    color: tuple
    alive: bool
    radius: float
    king: bool


    def render(self, screen) -> None:
        """Renders the hexagon on the screen"""
        x,y = self.center
        pg.draw.circle(screen, self.color, (x+1.1,y+1), self.radius)