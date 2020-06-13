from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.text_variable import text_variable
from FrontEnd.Elements.SingleInputBox import InputBox
import pygame

class ModifyBar(Element):
    bg = pygame.transform.smoothscale(pygame.image.load('./resources/SessionWinUI/bg/transparent_bg.png'), (300, 40))
    # bg = pygame.Surface((300, 40))
    bg.fill((255,255,255))

    def __init__(self, process, location, title, content, fontsize):
        Element.__init__(self, process)
        self.location = location
        self.surface = ModifyBar.bg
        self.title = self.createChild(text_variable, (0, 10), title+":", 'simhei', fontsize, (112,112,112))
        self.inputBox = self.createChild(InputBox, (120, 8), 150, 'simhei', 22, (0, 0, 0), (200, 200, 200))
        self.inputBox.text = content

        # self.font = pygame.font.SysFont('simhei', fontsize)
        # self.title = self.font.render(title+":", True, (112, 112, 112))
        # if content == None:
        #     self.content = self.font.render("无", True, (0, 0, 0))
        # else:
        #     self.content = self.font.render(content, True, (0, 0, 0))

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])