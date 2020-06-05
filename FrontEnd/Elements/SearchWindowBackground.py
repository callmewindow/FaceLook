from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.SearchPeopleOrGroup import SearchPeopleOrGroup
from FrontEnd.Elements.SearchPeople import SearchPeople
import pygame


class SearchWindowBackground(Element):

    def __init__(self, process):
        Element.__init__(self, process)
        self.surface = pygame.Surface((700, 450))
        self.surface.fill((255, 255, 255))
        self.location = (0, 0)

    def init(self):
        self.SearchFriendOrGroup = self.createChild(SearchPeopleOrGroup, (0, 0))
        self.SearchPeople = self.createChild(SearchPeople, (0, 50))

    def getEvent(self, event):
        for child in self.childs:
            if child.active:
                child.getEvent(event)

    def update(self):
        for child in self.childs:
            if child.active:
                child.update()
