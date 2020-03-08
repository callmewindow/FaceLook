from FrontEnd.Elements.Element import Element
import pygame
from Common.base import *
class CandyButton(Element):
    source_img = pygame.image.load('./resources/candy.png')
    image = pygame.transform.smoothscale(source_img,(100,50))
    bigImage = pygame.transform.smoothscale(source_img,(120,60))
    del source_img
    def __init__(self,process,location):
        Element.__init__(self,process)
        self.surface = CandyButton.image        
        self.smallSize = (100,50)
        self.smallLocation = location
        self.bigSize = (140,70)
        self.bigLocation = (location[0]-10,location[1]-5)        
        self.location = location
        self.size = self.smallSize
    def posin(self,pos):
        x = pos[0]
        y = pos[1]
        if self.location[0]<=x and x<=self.location[0]+self.size[0] and self.location[1]<=y and y<=self.location[1]+self.size[1]:
            return True
        return False
    def getEvent(self,event):
        if event.type == pygame.constants.MOUSEMOTION:
            if self.posin(event.pos):
                self.size = self.bigSize
                self.location = self.bigLocation
                self.surface = CandyButton.bigImage
            else:
                self.size = self.smallSize
                self.location = self.smallLocation
                self.surface = CandyButton.image
            return
        if event.type == pygame.constants.MOUSEBUTTONDOWN:
            if self.posin(event.pos):
                self.process.addAction(Action(ActionType.LOGIN,None))
            
        