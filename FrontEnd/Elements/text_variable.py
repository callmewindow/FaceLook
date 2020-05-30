from FrontEnd.Elements.Element import Element
import pygame

class text_variable(Element):
    def __init__(self, process, location, text, fonttype, fontsize, color):
        Element.__init__(self, process)
        self.font = pygame.font.SysFont(fonttype, fontsize)
        # print(pygame.font.get_fonts())
        self.location = location
        if text == None:
            self.surface = self.font.render("无",True,color)
        else:
            self.surface = self.font.render(text,True,color)
    