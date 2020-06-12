from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.FriendList import FriendList
from FrontEnd.Elements.SelfInfo import SelfInfo
from FrontEnd.Elements.SearchBar import SearchBar
from FrontEnd.Elements.SwitchListBar import SwitchListBar
from FrontEnd.Elements.SearchResult import SearchResult
from FrontEnd.Elements.MainMenubar import MainMenubar
from FrontEnd.Elements.CreateGroup import CreateGroup
from FrontEnd.Elements.Button import UserCloseButton, UserMinimizeButton
from Common.base import readData
import pygame


class UserWindowBackground(Element):

    def __init__(self, process):
        Element.__init__(self, process)
        self.surface = pygame.Surface((350, 740))
        self.surface.fill((255, 255, 255))
        self.location = (0, 0)
        self.displayed_list = 0
        self.self_info = self.createChild(SelfInfo, (0, 0))
        self.search_bar = self.createChild(SearchBar, (0, 119))
        self.friend_list = self.createChild(FriendList, (0, 200), 0)
        self.group_list = self.createChild(FriendList, (350, 200), 1)
        self.switch_list_bar = self.createChild(SwitchListBar, (0, 155))
        self.search_result = self.createChild(SearchResult, (0, 155))
        self.create_group = self.createChild(CreateGroup, (25, 550))
        self.search_result.refresh('', self.friend_list, self.group_list)
        self.main_menubar = self.createChild(MainMenubar, (0, 700))
        self.closeButton = self.createChild(UserCloseButton, (315, 8))
        self.minimizeButton = self.createChild(UserMinimizeButton, (280, 8))

    def getEvent(self, event):
        if self.search_bar.input.focused and event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN,
                                                                                            pygame.K_KP_ENTER]:
            self.search_result.refresh(self.search_bar.get_text(), self.friend_list, self.group_list)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 0 <= event.pos[0] <= 350 and 0 <= event.pos[1] <= 119:
                self.switch_list_bar.enable()
                if self.displayed_list == 0:
                    self.friend_list.enable()
                else:
                    self.group_list.enable()
                self.search_bar.input.text = ''
                self.search_result.disable()
        for child in self.childs:
            if child.active:
                child.getEvent(event)

    def update(self):
        if self.switch_list_bar.changed:
            self.friend_list.enable()
            self.group_list.enable()
            if self.displayed_list == 0 and self.group_list.location[0] > 0:
                self.friend_list.location = (self.friend_list.location[0] - 35, 200)
                self.group_list.location = (self.group_list.location[0] - 35, 200)
            elif self.displayed_list == 1 and self.friend_list.location[0] < 0:
                self.friend_list.location = (self.friend_list.location[0] + 35, 200)
                self.group_list.location = (self.group_list.location[0] + 35, 200)
            else:
                self.switch_list_bar.changed = False
                self.displayed_list = 1 - self.displayed_list
                if self.displayed_list == 0:
                    self.group_list.disable()
                else:
                    self.friend_list.disable()

        if self.search_bar.input.focused:
            self.switch_list_bar.disable()
            self.friend_list.disable()
            self.group_list.disable()
            self.search_result.enable()

        if self.main_menubar.create_button.pressed:
            self.main_menubar.create_button.pressed = False
            self.friend_list.frozen = True
            self.group_list.frozen = True
            self.create_group.enable()
        if not self.create_group.active:
            self.friend_list.frozen = False
            self.group_list.frozen = False
        for child in self.childs:
            if child.active:
                child.update()
