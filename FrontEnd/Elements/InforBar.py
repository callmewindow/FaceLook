from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.text_default import text_default
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
        self.haveTitle = True
        if title == "" :
            self.haveTitle = False
        self.title = self.font.render(title+":", True, (112, 112, 112))
        self.content = self.font.render(content, True, (0, 0, 0))

    def display(self):
        surface = self.surface.copy()
        # 上边距为10时20字号恰好居中
        if self.haveTitle:
            surface.blit(self.title, (0, 10))
        surface.blit(self.content, (80, 10))
        return surface


    
    