import pygame
class Element():
    listens = []
    def __init__(self,process):
        self.parent = None
        self.childs = []
        self.state = 0
        self.counter = 0
        self.surface = None
        self.process = process
        self.active = True
    def getEvent(self,event):
        for child in self.childs:
            if child.active:
                child.getEvent(event)
    def createChild(self,childType,*args,**kwargs):
        child = childType(self.process,*args,**kwargs)
        self.childs.append(child)
        return child
    def update(self):
        for child in self.childs:
            if child.active:
                child.update()
    def display(self):
        surface = pygame.Surface.copy(self.surface)
        for child in self.childs:
            if child.active:
                surface.blit(child.display(),child.location)
        return surface
    def switchState(self,state):
        self.state = state
        self.counter = 0