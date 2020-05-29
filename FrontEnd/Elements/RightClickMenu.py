from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.RightClickMenuBlock import RightClickMenuBlock
import pygame


class RightClickMenu(Element):

    def __init__(self, process):
        Element.__init__(self, process)
        self.disable()
        self.location = (0, 0)
        self.blocks = []
        for i in range(4):
            self.blocks.append(self.createChild(RightClickMenuBlock, (1, 1 + i * 40), i))
        self.surface = pygame.image.load('./resources/UserWindowUI/friend_right_menu.png')
        self.size = (122, 162)
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
        if x > 228:
            x = 228
        if y > 338:
            y = 338
        self.location = (x, y)

    def set_user(self, user):
        for block in self.blocks:
            block.set_user(user)
