import pygame
from FrontEnd.Elements.Element import Element

class SessionWindowBackground(Element):
    def __init__(self,process):
        Element.__init__(self,process)
        self.location = (0,0)
        self.surface = pygame.Surface((780,480))
        self.surface.fill((128,0,128))
        #aqua = self.createChild(Aqua,(450,300))
    
        
        
        
        
