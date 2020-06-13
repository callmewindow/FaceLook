from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.FriendList import FriendBlock, GroupBlock
import pygame


class Title(Element):
    image_friend = pygame.image.load('./resources/UserWindowUI/search_friend.png')
    image_group = pygame.image.load('./resources/UserWindowUI/search_group.png')

    def __init__(self, process, location, title_type):
        Element.__init__(self, process)
        self.location = location
        if title_type == 0:
            self.surface = Title.image_friend
        elif title_type == 1:
            self.surface = Title.image_group


class SearchResult(Element):
    stupid_hint = pygame.image.load('./resources/UserWindowUI/support_to_search.png')
    image = pygame.Surface((350, 550))
    image.fill((255, 255, 255))

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.disable()
        self.location = location
        self.friend_list = None
        self.group_list = None
        self.surface = SearchResult.image
        self.index = 0
        self.blank = True

    def refresh(self, keyword, friend_list, group_list):
        self.childs.clear()
        if keyword == '':
            self.blank = True
            return
        self.blank = False
        self.createChild(Title, (0, 0), 0)
        index_ = 0
        for friend in friend_list.childs:
            if keyword in friend.user['username'] or keyword in friend.user['nickname']:
                self.createChild(FriendBlock, (0, index_ * 100 + 50), friend.user)
                index_ += 1
        base = 150 if index_ == 0 else index_ * 100 + 100
        self.createChild(Title, (0, base - 50), 1)
        index_ = 0
        for group in group_list.childs:
            if keyword in group.group['sessionName']:
                self.createChild(GroupBlock, (0, index_ * 100 + base), group.group)
                index_ += 1

    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        if self.blank:
            surface.blit(SearchResult.stupid_hint, (0, 0))
        return surface

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_WHEELDOWN and self.index <= len(self.childs) - 7:
                self.index += 1
                for child in self.childs:
                    child.location = (child.location[0], child.location[1] - 100)
            if event.button == pygame.BUTTON_WHEELUP and self.index > 0:
                self.index -= 1
                for child in self.childs:
                    child.location = (child.location[0], child.location[1] + 100)

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            if child.active:
                child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])
