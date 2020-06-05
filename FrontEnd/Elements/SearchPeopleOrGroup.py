from FrontEnd.Elements.Element import Element
import pygame


class SearchPeopleOrGroup(Element):
    # state == 0 找人
    # state == 1 找群
    image_people = pygame.image.load('./resources/SearchWindowUI/search_people.png')
    image_group = pygame.image.load('./resources/SearchWindowUI/search_group.png')

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (800, 50)
        self.surface = SearchPeopleOrGroup.image_people
        self.state = 0

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.pos_in(event.pos) == 1:
                self.surface = SearchPeopleOrGroup.image_people
                self.state = 0
            elif self.pos_in(event.pos) == 2:
                self.surface = SearchPeopleOrGroup.image_group
                self.state = 1

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if 0 < y < self.size[1]:
            if 0 < x < self.size[0] // 2:
                return 1
            elif self.size[0] // 2 < x < self.size[0]:
                return 2
        return 0
