from FrontEnd.Elements.Element import Element
import pygame
class Avatar(Element):
    def __init__(self,process,location,surface):
        Element.__init__(self,process)
        self.location = location
        self.surface = surface
    def update(self):
        pass