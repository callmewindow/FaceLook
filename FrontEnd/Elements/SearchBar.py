from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.SingleInputBox import InputBox
import pygame


class SearchBar(Element):
    #searchIcon = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/search.png'), (20, 20))
    searchIcon = pygame.image.load('./resources/UserWindowUI/search_icon.png')
    image = pygame.image.load('./resources/UserWindowUI/search_bar.png')
    image_white = pygame.Surface((350, 36))
    image_white.fill((255, 255, 255))

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (350, 36)
        self.input = self.createChild(InputBox, (36, 5), 300, 'dengxian', 24, (0, 0, 0), (255, 255, 255))
        self.surface = SearchBar.image
        self.input.disable()

    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        surface.blit(SearchBar.searchIcon, (8, 8))
        return surface

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.pos_in(event.pos):
                self.input.enable()
                self.surface = SearchBar.image_white
            else:
                self.input.disable()
                self.surface = SearchBar.image
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def get_text(self):
        return self.input.get_text()

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] <= x <= self.location[0] + self.size[0] \
                and self.location[1] <= y <= self.location[1] + self.size[1]:
            return True
        return False
