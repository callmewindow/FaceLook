from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.SearchPeopleOrGroup import SearchPeopleOrGroup
from FrontEnd.Elements.SearchPeople import SearchPeople
from FrontEnd.Elements.SearchGroup import SearchGroup
import pygame


class SearchWindowBackground(Element):

    def __init__(self, process):
        Element.__init__(self, process)
        self.surface = pygame.Surface((800, 450))
        self.surface.fill((255, 255, 255))
        self.location = (0, 0)
        self.search_people_group = self.createChild(SearchPeopleOrGroup, (0, 0))
        self.search_people = self.createChild(SearchPeople, (0, 50))
        self.search_group = self.createChild(SearchGroup, (0, 50))
        self.search_group.disable()

    def getEvent(self, event):
        for child in self.childs:
            if child.active:
                child.getEvent(event)

    def update(self):
        if self.search_people_group.state == 0:
            self.search_group.disable()
            self.search_people.enable()
        else:
            self.search_people.disable()
            self.search_group.enable()

        for child in self.childs:
            if child.active:
                child.update()
