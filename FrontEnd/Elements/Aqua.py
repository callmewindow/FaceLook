from FrontEnd.Elements.Element import Element
import pygame
class Aqua(Element):
    images = []
    for _ in range(0,20):
        url = './resources/Aqua/aqua '+str(_)+'.png'
        images.append(pygame.image.load(url))
    def __init__(self,location):
        Element.__init__(self)
        self.location = location
        self.surface = Aqua.images[0]
    def update(self):
        if self.state == 0:
            return
        if self.state == 1:
            self.counter = (self.counter+1)%100        
            self.surface = Aqua.images[self.counter//5]
            return
    def onClick(self):
        if self.state == 0:
            self.state = 1
            return
        if self.state == 1:
            self.state = 0
            return
    def getEvent(self,event):
        if event.type == pygame.constants.MOUSEBUTTONDOWN:
            print('AAAAA')
            self.onClick()
        if event.type == pygame.constants.KEYDOWN:
            self.process.addAction(0)
            print(self.process.actionList)