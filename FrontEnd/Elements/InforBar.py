from FrontEnd.Elements.Element import Element
import pygame

class InforBar(Element):
    pygame.font.init()

    bg = pygame.Surface((300, 40))
    bg.fill((255, 255, 255))

    def __init__(self, process, location, title, content, fontsize):
        Element.__init__(self, process)
        self.location = location
        self.surface = InforBar.bg
        self.font = pygame.font.SysFont('simhei', fontsize)
        self.title = self.font.render(title+":", True, (112, 112, 112))
        if content == None:
            self.content = self.font.render("无", True, (0, 0, 0))
        else:
            self.content = self.font.render(content, True, (0, 0, 0))

    def display(self):
        surface = self.surface.copy()
        surface.blit(self.title, (0, 10))
        surface.blit(self.content, (80, 10))
        return surface
