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
        self.testBlock = self.createChild(FriendBlock,(0,0),(350,150),self.process.data.user)
        self.testBlock2 = self.createChild(FriendBlock,(0,150),(350,150),self.process.data.user)
        self.testBlock3 = self.createChild(FriendBlock,(0,300),(350,150),self.process.data.user)
        self.testBlock4 = self.createChild(FriendBlock,(0,450),(350,150),self.process.data.user)
        self.testBlock5 = self.createChild(FriendBlock,(0,600),(350,150),self.process.data.user)

        