import pygame
from Common.base import *
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.InputArea import InputArea
class UnitTestBackground(Element):

    def __init__(self,process):
        Element.__init__(self,process)
        self.location = (0,0)
        self.state = 0
        self.counter = 0
        self.surface = pygame.Surface((600,450))
        self.surface.fill((200,200,200))
        self.createChild(InputArea,(50,50), (300,300), 'dengxian', 30, (0,0,0), (128,128,128))
    def getMessage(self, message):
        pass
    def update(self):        
        Element.update(self)
    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        return surface
          
        
        
