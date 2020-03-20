import pygame
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Inputbox_default import Inputbox_default


class SearchBar(Element):
    searchIcon = pygame.image.load('./resources/searchicon.png')
    image = pygame.Surface((350, 55))
    image.fill((255, 255, 255))

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (350, 55)
        self.searchInputbox = self.createChild(Inputbox_default, (50, 0))
        self.icon = SearchBar.searchIcon
        self.surface = SearchBar.image
        self.searchInputbox.enable()

    def display(self):
        surface = pygame.Surface.copy(self.surface)
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        surface.blit(self.icon, (10, 10))
        return surface

    def getEvent(self, event):
        if event.type == pygame.constants.MOUSEBUTTONDOWN or event.type == pygame.constants.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.constants.MOUSEBUTTONDOWN or event.type == pygame.constants.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])
