from FrontEnd.Elements.Element import Element
import pygame
class text_default(Element):
    font = pygame.font.SysFont('DENGXIAN',25)
    def __init__(self,process,location,text,color):
        Element.__init__(self,process)
        self.location = location
        self.surface = text_default.font.render(text,True,color)
        self.text = text
        self.color = color
    def alignCenter(self,pos):
        x = pos[0]
        y = pos[1]
        rect = self.surface.get_rect()
        rectX = rect[2]
        rectY = rect[3]
        self.location = (x-rectX//2,y-rectY//2)
    def setText(self,text):
        self.text = text
        rect = self.surface.get_rect()
        self.surface = text_default.font.render(text,True,self.color)        
        rectX = rect[2]
        rectY = rect[3]
        center = (self.location[0]+rectX//2,self.location[1]+rectY//2)
        self.alignCenter(center)
    