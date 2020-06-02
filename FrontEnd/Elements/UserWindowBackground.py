from Common.base import User, UserStateType
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.FriendList import FriendList
from FrontEnd.Elements.SelfInfo import SelfInfo
from FrontEnd.Elements.SearchBar import SearchBar
from FrontEnd.Elements.SwitchListBar import SwitchListBar
from FrontEnd.Elements.SearchResult import SearchResult
from FrontEnd.Elements.MainMenubar import MainMenubar
from FrontEnd.Elements.MainMenu import MainMenu
from FrontEnd.Elements.InputArea import InputArea
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
        self.switchListBar = self.createChild(SwitchListBar, (0, 155))
        self.searchResult = self.createChild(SearchResult, (0, 155), self.process.data.getFriendList(),
                                             self.process.data.getGroupList())
        self.mainMenu = self.createChild(MainMenu, (0, 700 - 80), self.process.data.getUser())
        self.mainMenubar = self.createChild(MainMenubar, (0, 700))
        #self.test = self.createChild(InputArea, (50, 50),(250,130),pygame.font.SysFont('DENGXIAN',24),(0,0,0),(255,255,255))

    def getEvent(self, event):
        if self.searchBar.input_box.focused and event.type == pygame.KEYDOWN and (
                event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
            self.searchResult.init(self.searchBar.get_text())
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 0 <= event.pos[0] <= 350 and 0 <= event.pos[1] <= 100:
                self.switchListBar.enable()
                self.friendList.enable()
                self.searchBar.input_box.text = ''
                self.searchResult.disable()

        for child in self.childs:
            if child.active:
                child.getEvent(event)

    def update(self):
        self.friendList.change_to = self.switchListBar.change_to
        self.friendList.has_changed = self.switchListBar.has_changed
        self.switchListBar.has_changed = False
        if self.searchBar.input_box.focused:
            self.switchListBar.disable()
            self.friendList.disable()
            self.searchResult.enable()
        if self.mainMenubar.get_state() == 2:
            self.friendList.frozen = True
            self.mainMenu.enable()
        else:
            self.friendList.frozen = False
            self.mainMenu.disable()

        for child in self.childs:
            if child.active:
                child.update()
