import pygame
from FrontEnd.Elements.Element import Element
from Common.base import Session
class MessageList(Element):
    def __init__(self,process):
        Element.__init__(self,process)
        
        
        print(self.process.data)
        self.surface = pygame.Surface((500,300))
        self.surface.fill((77,77,0))
        self.location = (50,50)

        self.index = 0
        
        
    def heartBeat(self):
        pass
class SessionWindowBackground(Element):
    def __init__(self,process):
        Element.__init__(self,process)
        self.location = (0,0)
        self.surface = pygame.Surface((780,480))
        self.surface.fill((128,0,128))
        self.createChild(MessageList)
        #aqua = self.createChild(Aqua,(450,300))
    
        
        
        
        
