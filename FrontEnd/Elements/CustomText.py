from FrontEnd.Elements.Element import Element
from typing import Tuple
import pygame


class CustomText(Element):

    def __init__(self, process, location, font: str, size: int, color: Tuple[int, int, int], text):
        Element.__init__(self, process)
        self.location = location
        self.size = size
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont(font, size)
        self.surface = self.font.render(text, True, color)

    def align_center(self, pos):
        x = pos[0]
        y = pos[1]
        rect = self.surface.get_rect()
        rect_x = rect[2]
        rect_y = rect[3]
        self.location = (x - rect_x // 2, y - rect_y // 2)

    def set_text(self, text):
        self.text = text
        # rect = self.surface.get_rect()
        self.surface = self.font.render(text, True, self.color)
        # rect_x = rect[2]
        # rect_y = rect[3]
        # center = (self.location[0] + rect_x // 2, self.location[1] + rect_y // 2)
        # self.align_center(center)

    def set_color(self, color: Tuple[int, int, int]):
        self.color = color
        self.surface = self.font.render(self.text, True, color)
