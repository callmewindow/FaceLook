from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.SingleClickButton import SingleClickButton
import pygame


class MainMenubar(Element):
    image = pygame.image.load('./resources/UserWindowUI/main_menu_bar.png')

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (350, 50)
        self.surface = MainMenubar.image
        self.createChild(SingleClickButton, (0, 0), (45, 40), (25, 25), './resources/UserWindowUI/friend_add.png', 'add')
        self.createChild(SingleClickButton, (45, 0), (45, 40), (25, 25), './resources/UserWindowUI/mail.png', 'apply')

    def getEvent(self, event):
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])
