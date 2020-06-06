from FrontEnd.Elements.Element import Element
from FrontEnd.Processes.SessionWindowProcess import createSession
import pygame
from Common.base import *
class Button(Element):
    source_img = pygame.image.load('./resources/WindowControlUI/user_close.png')
    image = pygame.transform.smoothscale(source_img,(32,32))
    bigImage = pygame.transform.smoothscale(source_img,(40,40))
    del source_img
    def __init__(self,process,location):
        Element.__init__(self,process)
        self.surface = self.image        
        self.smallSize = (32,32)
        self.smallLocation = location
        self.bigSize = (40,40)
        self.bigLocation = (location[0]-(self.bigSize[0]-self.smallSize[0])/2,location[1]-(self.bigSize[1]-self.smallSize[1])/2)        
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
                self.surface = self.bigImage
            else:
                self.size = self.smallSize
                self.location = self.smallLocation
                self.surface = self.image
            return
        if event.type == pygame.constants.MOUSEBUTTONDOWN and event.button == pygame.constants.BUTTON_LEFT and self.posin(event.pos):
            self.onClick()
    def onClick(self):
        pass
class CloseButton(Button):
    def onClick(self):
        self.process.stop()
        self.process.dragging = False
class MinimizeButton(Button):
    source_img = pygame.image.load('./resources/WindowControlUI/user_move.png')
    image = pygame.transform.smoothscale(source_img,(32,32))
    bigImage = pygame.transform.smoothscale(source_img,(40,40))
    def onClick(self):
        self.process.minimize()
        self.process.dragging = False

class UserCloseButton(Button):
    source_img = pygame.image.load('./resources/WindowControlUI/user_close.png')
    image = pygame.transform.smoothscale(source_img,(24,24))
    bigImage = pygame.transform.smoothscale(source_img,(30,30))

    def __init__(self, process, location):
        Button.__init__(self,process,location)
        self.surface = self.image
        self.smallSize = (24, 24)
        self.smallLocation = location
        self.bigSize = (30, 30)
        self.bigLocation = (location[0] - (self.bigSize[0] - self.smallSize[0]) / 2,
                            location[1] - (self.bigSize[1] - self.smallSize[1]) / 2)
        self.location = location
        self.size = self.smallSize

    def onClick(self):
        self.process.stop()
        self.process.dragging = False

class UserMinimizeButton(UserCloseButton):
    source_img = pygame.image.load('./resources/WindowControlUI/user_move.png')
    image = pygame.transform.smoothscale(source_img,(24,24))
    bigImage = pygame.transform.smoothscale(source_img,(30,30))

    def onClick(self):
        self.process.minimize()
        self.process.dragging = False
    


            
        