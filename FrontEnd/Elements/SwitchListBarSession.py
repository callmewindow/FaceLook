from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.IconChangeButton import IconChangeButton
import pygame


class SwitchListBarSession(Element):
    # state==0 idle
    # state==1 hover
    # state==2 select
    image = pygame.Surface((340, 50))
    image.fill((255,255,255))
    # image = pygame.transform.smoothscale(pygame.image.load('./resources/SessionWinUI/bg/transparent_bg.png'), (340, 50))
    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (340, 50)
        self.buttonSize = (85, 50)
        self.icon1 = self.createChild(IconChangeButton, (0, 0), './resources/SessionWinUI/icons/message.png', './resources/SessionWinUI/icons/message_wh.png', self.buttonSize)
        self.icon2 = self.createChild(IconChangeButton, (85, 0), './resources/SessionWinUI/icons/file.png', './resources/SessionWinUI/icons/file_wh.png', self.buttonSize)
        self.icon3 = self.createChild(IconChangeButton, (2*85, 0), './resources/SessionWinUI/icons/phone.png', './resources/SessionWinUI/icons/phone_wh.png', self.buttonSize)
        self.icon4 = self.createChild(IconChangeButton, (3*85, 0), './resources/SessionWinUI/icons/video.png', './resources/SessionWinUI/icons/video_wh.png', self.buttonSize)
        self.icon = [self.icon1, self.icon2, self.icon3, self.icon4]

        self.surface = SwitchListBarSession.image
        self.buttonState = [2, 0, 0, 0]
        self.icon[0].setState(self.buttonState[0])

        self.buttonLocation = [0, 85, 2*85, 3*85]
        self.change_from = 0
        self.change_to = 0

    def pos_in(self, pos, index):
        x = pos[0]
        y = pos[1]
        if self.buttonLocation[index] < x < self.buttonLocation[index] + self.buttonSize[0] and \
                0 < y < self.buttonSize[1]:
            return True
        return False

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        if event.type == pygame.MOUSEMOTION:
            for i in range(4):
                if self.buttonState[i] != 2:
                    if self.pos_in(event.pos, i):
                        self.buttonState[i] = 1
                    else:
                        self.buttonState[i] = 0
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            for i in range(4):
                if self.pos_in(event.pos, i):
                    if not i == 0:
                        # 禁止切换
                        # self.process.createAlertWindow("功能暂未开放")
                        pass
                    else:
                        self.buttonState = [0, 0, 0, 0]
                        self.buttonState[i] = 2
                        self.change_to = i

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def display(self):
        surface = self.surface.copy()
        for i in range(4):
            self.icon[i].setState(self.buttonState[i])

        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        return surface
