import pygame
from FrontEnd.Elements.Element import Element
class Window(Element):
    def __init__(self,caption,size,color,process):
        Element.__init__(self)
        pygame.display.set_caption(caption)        
        self.FPSClock=pygame.time.Clock()
        self.surface = pygame.display.set_mode(size)
        self.surface.fill(color)
        self.process = process
    def display(self):
        self.update()
        for child in self.childs:
            self.surface.blit(child.display(),child.location)