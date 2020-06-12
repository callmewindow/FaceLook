import pygame
from Common.base import *
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.text_variable import text_variable
from FrontEnd.Elements.TextAreaVariable import TextAreaVariable
from FrontEnd.Elements.TextButton import TextButton
from FrontEnd.Elements.Button import UserCloseButton

class AlertWindowBackground(Element):
    def __init__(self, process):
        Element.__init__(self, process)
        self.surface = pygame.Surface((350, 200))
        self.surface.fill((251, 114, 153))
        self.location = (0, 0)

        # 绘制上半部分内容
        self.title = self.createChild(text_variable,(10,15),"提示",'simhei',18,(255,255,255),True)
        self.alert = self.createChild(TextAreaVariable,(25,50),300,0,'./resources/SessionWinUI/bg/transparent_bg.png','simhei',20,self.process.content,(255,255,255))
        self.closeButton = self.createChild(UserCloseButton, (310, 12))
        self.yesButton = self.createChild(TextButton, (260, 150), "了解", 18, (80, 40))

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            if child.active:
                child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])
        
        # 修改信息
        if self.yesButton.state == 2:
            self.yesButton.setState(0)
            self.closeButton.onClick()