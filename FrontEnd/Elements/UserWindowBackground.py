from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Avatar import Avatar
from FrontEnd.Elements.FriendList import *
from FrontEnd.Elements.text_default import *
from FrontEnd.Elements.SelfInfo import *
from FrontEnd.Elements.SearchBar import *
from FrontEnd.Elements.MenuBar import *
import pygame


class UserWindowBackground(Element):
    def __init__(self, process):
        Element.__init__(self, process)
        self.surface = pygame.Surface((350, 700))
        self.surface.fill((255, 255, 255))
        self.location = (0, 0)

    def init(self):
        self.selfInfo = self.createChild(SelfInfo, (0, 0), self.process.data.user)
        self.searchBar = self.createChild(SearchBar, (0, 100))
        self.menuBar = self.createChild(MenuBar, (0, 155))
        # self.logo = self.createChild(text_default, (0, 0), '0 Message(s), 0 Invitation(s)', (0, 0, 0))
        # self.logo.alignCenter((175, 50))
        self.friendList = self.createChild(FriendList, (0, 200), self.process.data.friendList)
