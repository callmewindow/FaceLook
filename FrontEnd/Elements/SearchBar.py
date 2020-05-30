import pygame
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Inputbox_blank import Inputbox_blank


class SearchBar(Element):
    searchIcon = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/search.png'), (32, 32))
    image = pygame.Surface((350, 55))
    image.fill((255, 255, 255))

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (350, 55)
        self.input_box = self.createChild(Inputbox_blank, (50, 8))
        self.icon = SearchBar.searchIcon
        self.surface = SearchBar.image
        self.input_box.enable()

    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        surface.blit(self.icon, (10, 10))
        return surface

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def get_text(self):
        return self.input_box.text
