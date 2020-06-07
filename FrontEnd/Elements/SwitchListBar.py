from FrontEnd.Elements.Element import Element
import pygame


class SwitchListBar(Element):
    # state==0 idle
    # state==1 hover
    # state==2 select
    image0 = pygame.image.load('./resources/UserWindowUI/switch_0.png')
    image1 = pygame.image.load('./resources/UserWindowUI/switch_1.png')
    icon0 = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/people.png'), (30, 30))
    #icon1 = pygame.image.load('./resources/UserWindowUI/group.png')
    icon1 = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/group.png'), (30, 30))
    icon0_h = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/people_black.png'), (30, 30))
    icon1_h = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/group_black.png'), (30, 30))
    icon0_s = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/people_blue.png'), (30, 30))
    icon1_s = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/group_blue.png'), (30, 30))

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (350, 45)
        self.buttonSize = (175, 45)
        self.icon = [SwitchListBar.icon0, SwitchListBar.icon1]
        self.icon_hover = [SwitchListBar.icon0_h, SwitchListBar.icon1_h]
        self.icon_select = [SwitchListBar.icon0_s, SwitchListBar.icon1_s]
        self.image = [SwitchListBar.image0, SwitchListBar.image1]
        self.buttonState = [2, 0]
        self.buttonLocation = [0, 175]
        self.changed = False
        self.surface = SwitchListBar.image0

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[1] < y < self.size[1] + self.location[1]:
            if 0 < x < self.size[0] // 2:
                return 0
            elif self.size[0] // 2 < x < self.size[0]:
                return 1
        return -1

    def getEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            target = self.pos_in(event.pos)
            if target == -1:
                if self.buttonState[0] != 2:
                    self.buttonState[0] = 0
                if self.buttonState[1] != 2:
                    self.buttonState[1] = 0
            if target != -1 and self.buttonState[target] != 2:
                self.buttonState[target] = 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            target = self.pos_in(event.pos)
            if target != -1 and self.buttonState[target] != 2:
                self.buttonState[target] = 2
                self.surface = self.image[target]
                self.buttonState[1 - target] = 0
                self.changed = True

    def display(self):
        surface = self.surface.copy()
        for i in range(2):
            if self.buttonState[i] == 0:
                surface.blit(self.icon[i], (self.buttonLocation[i] + 72, 7))
            elif self.buttonState[i] == 1:
                surface.blit(self.icon_hover[i], (self.buttonLocation[i] + 72, 7))
            else:
                surface.blit(self.icon_select[i], (self.buttonLocation[i] + 72, 7))
        return surface
