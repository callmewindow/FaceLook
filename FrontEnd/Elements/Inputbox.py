from FrontEnd.Elements.Element import Element
import pygame
class Inputbox(Element):
    def __init__(self,process,location,size,font,fontSize):
        Element.__init__(self,process)
        self.text = ''
        self.focused = False
        self.location = location
        self.surface = pygame.Surface(size)
        self.font = pygame.font.Font(font,fontSize)
        self.editIndex = 0
    def addChar(self,ch):
        pass
    def removeChar(self):
        pass
    def update(self):
        pass
    def getEvent(self,event):
        pass
    
    