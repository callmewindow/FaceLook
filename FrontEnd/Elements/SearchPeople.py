from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.DropDownMenu import DropDownMenu
from FrontEnd.Elements.SingleInputBox import InputBox
from FrontEnd.Elements.TextButton import TextButton

import pygame


class SearchPeople(Element):

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.surface = pygame.Surface((700, 400))
        self.surface.fill((255, 255, 255))
        self.location = location
        self.menu = self.createChild(DropDownMenu, (50, 50), ['用户名', '昵称', '手机号', '邮箱'])
        self.input = self.createChild(InputBox,(200,50), 350,'dengxian', 25, (0,0,0),(255,255,255))
        self.search_button = self.createChild(TextButton,(580,50),'搜索',20,(80,30))

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])
