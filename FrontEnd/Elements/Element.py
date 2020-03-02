import pygame
class Element():
    listens = []
    def __init__(self):
        self.parent = None
        self.childs = []
        self.state = 0
        self.counter = 0
        self.surface = None
        self.process = None
    def getEvent(self,event):
        for child in self.childs:
            child.getEvent(event)
    def createChild(self,childType,*args,**kwargs):
        child = childType(*args,**kwargs)
        child.process = self.process
        self.childs.append(child)
    def update(self):
        for child in self.childs:
            child.update()
    def display(self):
        surface = pygame.Surface.copy(self.surface)
        for child in self.childs:
            surface.blit(child.surface,child.location)
        return surface
    def switchState(self,state):
        self.state = state
        self.counter = 0