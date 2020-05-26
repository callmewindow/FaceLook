from FrontEnd.Elements.Element import Element
import pygame


class Image(Element):
    def __init__(self, process, location, size, url):
        Element.__init__(self, process)
        self.location = location
        self.url = url
        self.surface = pygame.surface((size))
        self.surface.fill((0,0,0))
    def load(self):
        pass

