from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Avatar import Avatar
from FrontEnd.Elements.FriendList import *
import pygame
class UserWindowBackground(Element):
    def __init__(self,process):
        Element.__init__(self,process)
        self.surface = pygame.Surface((350,700))
        self.surface.fill((255,255,255))
        self.location = (0,0)

    def init(self):
        self.friendList = self.createChild(FriendList,(0,100),self.process.data.friendList)

        