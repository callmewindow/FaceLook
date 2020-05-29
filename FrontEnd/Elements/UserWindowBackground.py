from Common.base import User, UserStateType
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.FriendList import FriendList
from FrontEnd.Elements.SelfInfo import SelfInfo
from FrontEnd.Elements.SearchBar import SearchBar
from FrontEnd.Elements.SwitchListBar import SwitchListBar
from FrontEnd.Elements.SearchResult import SearchResult
from FrontEnd.Elements.MainMenubar import MainMenubar
from FrontEnd.Elements.MainMenu import MainMenu
import pygame


class UserWindowBackground(Element):

    def __init__(self, process):
        Element.__init__(self, process)
        self.surface = pygame.Surface((350, 740))
        self.surface.fill((255, 255, 255))
        self.location = (0, 0)

    def init(self):
        self.selfInfo = self.createChild(SelfInfo, (0, 0), self.process.data.getUser())
        self.searchBar = self.createChild(SearchBar, (0, 100))
        self.friendList = self.createChild(FriendList, (0, 200), self.process.data.getFriendList(),
                                           self.process.data.getGroupList(), self.process.data.getMessageList())
        self.switchListBar = self.createChild(SwitchListBar, (0, 155), self.friendList)
        self.searchResult = self.createChild(SearchResult, (0, 155))
        self.mainMenu = self.createChild(MainMenu, (0, 700 - 80), self.process.data.getUser())
        self.mainMenubar = self.createChild(MainMenubar, (0, 700))

    def getEvent(self, event):
        if self.searchBar.searchInputbox.focused and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.searchResult.enable()
            self.searchResult.init([],
                                   [User('Mea', 'Mea', '群搜索结果1', "image::DEFUALT_MEA", UserStateType.ONLINE),
                                    User('Mea', 'Mea', '群搜索结果2', "image::DEFUALT_MEA", UserStateType.ONLINE),
                                    User('Mea', 'Mea', '群搜索结果3', "image::DEFUALT_MEA", UserStateType.ONLINE)])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 0 <= event.pos[0] <= 350 and 0 <= event.pos[1] <= 100:
                self.switchListBar.enable()
                self.friendList.enable()
                self.searchBar.searchInputbox.text = ''
                self.searchResult.disable()

        for child in self.childs:
            if child.active:
                child.getEvent(event)

    def update(self):
        if self.searchBar.searchInputbox.focused:
            self.switchListBar.disable()
            self.friendList.disable()
            self.mainMenu.disable()
        if self.mainMenubar.get_state() == 2:
            self.friendList.freeze()
            self.mainMenu.enable()
        else:
            self.friendList.unfreeze()
            self.mainMenu.disable()

        for child in self.childs:
            if child.active:
                child.update()
