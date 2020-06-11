from FrontEnd.Elements.Element import Element
import pygame


class text_variable(Element):
    def __init__(self, process, location, text, fonttype, fontsize, color, setBold=False):
        Element.__init__(self, process)
        self.font = pygame.font.SysFont(fonttype, fontsize)
        self.font.set_bold(setBold)
        self.location = location
        if text == None:
            tempText = "无"
        else:
            tempText = text
        self.surface = self.font.render(tempText, True, color)
        self.text = tempText
        self.color = color

    def alignCenter(self, pos):
        x = pos[0]
        y = pos[1]
        rect = self.surface.get_rect()
        rectX = rect[2]
        rectY = rect[3]
        self.location = (x-rectX//2, y-rectY//2)

    def setText(self, text):
        self.text = text
        rect = self.surface.get_rect()
        self.surface = self.font.render(text, True, self.color)
        # rectX = rect[2]
        # rectY = rect[3]
        # center = (self.location[0]+rectX//2, self.location[1]+rectY//2)
        # self.alignCenter(center)
