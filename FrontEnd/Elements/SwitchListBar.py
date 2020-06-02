from FrontEnd.Elements.Element import Element
import pygame


class SwitchListBar(Element):
    # state==0 idle
    # state==1 hover
    # state==2 select
    image0 = pygame.image.load('./resources/UserWindowUI/switch_0.png')
    image1 = pygame.image.load('./resources/UserWindowUI/switch_1.png')
    image2 = pygame.image.load('./resources/UserWindowUI/switch_2.png')
    icon1 = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/message.png'), (30, 30))
    icon2 = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/people.png'), (30, 30))
    icon3 = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/group.png'), (30, 30))
    icon1_h = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/message_black.png'), (30, 30))
    icon2_h = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/people_black.png'), (30, 30))
    icon3_h = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/group_black.png'), (30, 30))
    icon1_s = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/message_blue.png'), (30, 30))
    icon2_s = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/people_blue.png'), (30, 30))
    icon3_s = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/group_blue.png'), (30, 30))

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (350, 45)
        self.buttonSize = (117, 45)
        self.icon = [SwitchListBar.icon1, SwitchListBar.icon2, SwitchListBar.icon3]
        self.icon_hover = [SwitchListBar.icon1_h, SwitchListBar.icon2_h, SwitchListBar.icon3_h]
        self.icon_select = [SwitchListBar.icon1_s, SwitchListBar.icon2_s, SwitchListBar.icon3_s]
        self.switch = [SwitchListBar.image0, SwitchListBar.image1, SwitchListBar.image2]
        self.surface = SwitchListBar.image0
        self.buttonState = [2, 0, 0]
        self.buttonLocation = [0, 117, 234]
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
            for i in range(3):
                if self.buttonState[i] != 2:
                    if self.pos_in(event.pos, i):
                        self.buttonState[i] = 1
                    else:
                        self.buttonState[i] = 0
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            for i in range(3):
                if self.pos_in(event.pos, i):
                    self.buttonState = [0, 0, 0]
                    self.buttonState[i] = 2
                    self.change_to = i
                    self.surface = self.switch[i]
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def display(self):
        surface = self.surface.copy()
        for i in range(3):
            if self.buttonState[i] == 0:
                surface.blit(self.icon[i], (self.buttonLocation[i] + 43, 7))
            elif self.buttonState[i] == 1:
                surface.blit(self.icon_hover[i], (self.buttonLocation[i] + 43, 7))
            else:
                surface.blit(self.icon_select[i], (self.buttonLocation[i] + 43, 7))

        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        return surface
