from FrontEnd.Elements.Element import Element
import pygame


class CustomText(Element):

    def __init__(self, process, location, font: str, size: int, color, text, width_limit=0):
        Element.__init__(self, process)
        self.location = location
        self.size = size
        self.color = color
        self.text = text
        self.width_limit = width_limit
        self.font = pygame.font.SysFont(font, size)
        if self.width_limit != 0:
            self.limit()
        self.surface = self.font.render(self.text, True, color)

    def set_text(self, text):
        self.text = text
        if self.width_limit != 0:
            self.limit()
        self.surface = self.font.render(text, True, self.color)

    def set_color(self, color):
        self.color = color
        self.surface = self.font.render(self.text, True, color)

    def limit(self):
        if self.font.size(self.text)[0] <= self.width_limit:
            return
        for i in range(len(self.text)):
            if self.font.size(self.text[:i + 1] + '...')[0] > self.width_limit:
                self.text = self.text[:i] + '...'
                break
