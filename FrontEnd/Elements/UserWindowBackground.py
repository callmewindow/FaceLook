from Common.base import User, UserStateType
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.FriendList import FriendList
from FrontEnd.Elements.SelfInfo import SelfInfo
from FrontEnd.Elements.SearchBar import SearchBar
from FrontEnd.Elements.MenuBar import MenuBar
from FrontEnd.Elements.SearchResult import SearchResult
import pygame


class UserWindowBackground(Element):
    def __init__(self, process):
        Element.__init__(self, process)
        self.surface = pygame.Surface((350, 700))
        self.surface.fill((255, 255, 255))
        self.location = (0, 0)

    def init(self):
        self.selfInfo = self.createChild(SelfInfo, (0, 0), self.process.data.getUser())
        self.searchBar = self.createChild(SearchBar, (0, 100))
        self.friendList = self.createChild(FriendList, (0, 200), self.process.data.getFriendList(),
                                           self.process.data.getGroupList(), self.process.data.getMessageList())
        self.menubar = self.createChild(MenuBar, (0, 155), self.friendList)
        self.searchResult = self.createChild(SearchResult, (0, 155))

    def getEvent(self, event):
        if self.searchBar.searchInputbox.focused and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.searchResult.enable()
            self.searchResult.init([],
                                   [User('Mea', 'Mea', '群搜索结果1', "image::DEFUALT_MEA", UserStateType.ONLINE),
                                    User('Mea', 'Mea', '群搜索结果2', "image::DEFUALT_MEA", UserStateType.ONLINE),
                                    User('Mea', 'Mea', '群搜索结果3', "image::DEFUALT_MEA", UserStateType.ONLINE)])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 0 <= event.pos[0] <= 350 and 0 <= event.pos[1] <= 100:
                self.menubar.enable()
                self.friendList.enable()
                self.searchBar.searchInputbox.text = ''
                self.searchResult.disable()

        for child in self.childs:
            if child.active:
                child.getEvent(event)

    def update(self):
        if self.searchBar.searchInputbox.focused:
            self.menubar.disable()
            self.friendList.disable()
        for child in self.childs:
            if child.active:
                child.update()
