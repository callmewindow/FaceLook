from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.RightClickMenuBlock import RightClickMenuBlock
import pygame


class RightClickMenu(Element):
    image = pygame.image.load('./resources/UserWindowUI/friend_right_menu.png')

    def __init__(self, process):
        Element.__init__(self, process)
        self.disable()
        self.location = (0, 0)
        self.blocks = []
        self.blocks.append(self.createChild(RightClickMenuBlock, (5, 5), 0))
        self.blocks.append(self.createChild(RightClickMenuBlock, (5, 45), 1))
        self.blocks.append(self.createChild(RightClickMenuBlock, (5, 85), 2))
        self.surface = RightClickMenu.image
        # self.surface.set_alpha(230)
        self.size = (130, 130)
        self.has_closed = False

    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            surface.blit(child.display(), child.location)
        return surface

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.pos_in(event.pos):
                self.has_closed = True
                self.disable()
            else:
                if event.button == pygame.BUTTON_LEFT:
                    self.has_closed = True
                    self.disable()
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def pos_in(self, pos):
        x, y = pos[0], pos[1]
        if self.location[0] <= x <= self.location[0] + self.size[0] \
                and self.location[1] <= y <= self.location[1] + self.size[1]:
            return True
        return False

    def change_location(self, location):
        x, y = location
        if x > 220:
            x = 220
        if y > 370:
            y = 370
        self.location = (x, y)

    def set_user(self, user):
        for block in self.blocks:
            block.set_user(user)
