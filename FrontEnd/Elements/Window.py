import pygame
from FrontEnd.Elements.Element import Element
class Window(Element):
    def __init__(self,process,caption,size,color):
        Element.__init__(self,process)
        self.color = color
        pygame.display.set_caption(caption)        
        self.FPSClock=pygame.time.Clock()
        self.surface = pygame.display.set_mode((600,450))
        self.surface.fill(color)
        #self.origin = pygame.Surface.copy(self.surface)
    def display(self):
        #self.surface.fill(self.color)
        self.update()
        for child in self.childs:
            self.surface.blit(child.display(),child.location)