from FrontEnd.Elements.Element import Element
import pygame


class CustomText(Element):

    def __init__(self, process, location, font: str, size: int, color, text):
        Element.__init__(self, process)
        self.location = location
        self.size = size
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont(font, size)
        self.surface = self.font.render(text, True, color)

    def set_text(self, text):
        self.text = text
        self.surface = self.font.render(text, True, self.color)

    def set_color(self, color):
        self.color = color
        self.surface = self.font.render(self.text, True, color)
