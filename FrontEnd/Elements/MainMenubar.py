from FrontEnd.Elements.Element import Element
import pygame


class MainMenubar(Element):
    image = pygame.Surface((350, 50))
    image.fill((255, 255, 255))

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (350, 40)
        self.surface = MainMenubar.image
        self.button = self.createChild(MenuButton, (5, 5))

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def get_state(self):
        return self.button.state


class MenuButton(Element):
    # 0 == idle
    # 1 == hover
    # 2 == select
    icon = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/apps.png'), (30, 30))
    icon_hover = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/apps_hover.png'), (30, 30))
    icon_select = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/apps_select.png'), (30, 30))

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.surface = MenuButton.icon
        self.location = location
        self.size = (30, 30)
        self.state = 0

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] < x < self.location[0] + self.size[0] and self.location[1] < y < self.location[1] + \
                self.size[1]:
            return True
        return False

    def getEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.state != 2:
                if self.pos_in(event.pos):
                    self.state = 1
                else:
                    self.state = 0
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.pos_in(event.pos):
                if self.state != 2:
                    self.state = 2
                else:
                    self.state = 1
            else:
                self.state = 0

    def update(self):
        if self.state == 0:
            self.surface = MenuButton.icon
        elif self.state == 1:
            self.surface = MenuButton.icon_hover
        else:
            self.surface = MenuButton.icon_select
