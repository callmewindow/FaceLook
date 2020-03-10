from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Avatar import Avatar
from FrontEnd.Elements.text_default import text_default
import pygame
class FriendBlock(Element):
    image = pygame.Surface((350,150))
    image.fill((255,255,255))
    image_onHover = pygame.Surface((350,150))
    image_onHover.fill((230,230,230))
    def __init__(self,process,location,size,user):
        Element.__init__(self,process)
        self.location = location
        self.size = size
        self.user = user
        self.avatar = self.createChild(Avatar,(25,25),(100,100),self.user.avatar)
        self.nicknameText = self.createChild(text_default,(200,75),self.user.nickname,(0,0,0))
        self.surface = FriendBlock.image
    def posin(self,pos):
        x = pos[0]
        y = pos[1]
        if self.location[0]<x and x<self.location[0]+self.size[0] and self.location[1]<y and y<self.location[1]+self.size[1]:
            return True
        return False
    def getEvent(self,event):
        if event.type == pygame.constants.MOUSEMOTION:
            if self.posin(event.pos):
                self.surface = FriendBlock.image_onHover
            else:
                self.surface = FriendBlock.image

class FriendList(Element):
    def __init__(self,process,location,friendList):
        Element.__init__(self,process)
        self.location = location
        self.friendList = friendList
    
    def update(self):
        if self.state == 0:
            return
