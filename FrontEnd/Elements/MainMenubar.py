from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Button_three import Button_three
import pygame


class MainMenubar(Element):
    image = pygame.Surface((350, 50))
    image.fill((255, 255, 255))

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (350, 40)
        self.surface = MainMenubar.image
        self.button = self.createChild(Button_three, (5,5), './resources/UserWindowUI/apps.png', \
            './resources/UserWindowUI/apps_hover.png', './resources/UserWindowUI/apps_select.png', (30, 30))

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def get_state(self):
        return self.button.state



