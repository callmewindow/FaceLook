from FrontEnd.Elements.Element import Element
import pygame
class text_default(Element):
    font = pygame.font.SysFont('DENGXIAN',25)
    def __init__(self,process,location,text,color):
        Element.__init__(self,process)
        self.location = location
        self.surface = text_default.font.render(text,True,color)
    def alignCenter(self,pos):
        x = pos[0]
        y = pos[1]
        rect = self.surface.get_rect()
        rectX = rect[2]
        rectY = rect[3]
        self.location = (x-rectX//2,y-rectY//2)
    