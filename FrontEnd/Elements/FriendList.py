from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Avatar import Avatar
from FrontEnd.Elements.text_default import text_default
import pygame
class FriendBlock(Element):
    image = pygame.Surface((350,150))
    image.fill((255,255,255))
    image_onHover = pygame.Surface((350,150))
    image_onHover.fill((245,245,245))
    image_onClick = pygame.Surface((350,150))
    image_onClick.fill((240,240,240))

    def __init__(self,process,location,user):
        Element.__init__(self,process)
        self.user = user
        self.avatar = self.createChild(Avatar,(25,25),self.user.avatar)
        userStateText = ' (online)' if self.user.state == 1 else ' (offline)'
        self.nicknameText = self.createChild(text_default,(150,75),self.user.nickname+userStateText,(0,0,0))
        self.surface = FriendBlock.image
        self.location = location
        self.size = (350,150)
    def posin(self,pos):
        x = pos[0]
        y = pos[1]
        if self.location[0]<x and x<self.location[0]+self.size[0] and self.location[1]<y and y<self.location[1]+self.size[1]:
            return True
        return False
    def getEvent(self,event):
        if event.type == pygame.constants.MOUSEMOTION and self.state!=2:
            if self.posin(event.pos):
                self.state = 1
                self.surface = FriendBlock.image_onHover
            else:
                self.state = 0
                self.surface = FriendBlock.image
            return
        if event.type == pygame.constants.MOUSEBUTTONDOWN and event.button == pygame.constants.BUTTON_LEFT:
            if self.posin(event.pos):
                self.state = 2
                self.surface = FriendBlock.image_onClick
            else:
                self.state = 0
                self.surface = FriendBlock.image

class FriendList(Element):
    listCover = pygame.image.load('./resources/listCover.png')
    listCoverY = -200
    def __init__(self,process,location,friendList):
        Element.__init__(self,process)
        self.location = location
        self.surface = pygame.Surface((350,600))
        self.friendList = friendList
        self.blocks = []
        for i in range(0,len(self.friendList)):
            user = self.friendList[i]
            self.blocks.append(self.createChild(FriendBlock,(0,i*150),user)) 
            print(self.blocks[i].location)       
        self.surface.fill((220,220,220))
        self.index = 0

    def display(self):
        surface = pygame.Surface.copy(self.surface)
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        if self.listCoverY < 600:
            self.listCoverY = self.listCoverY + 8
            surface.blit(self.listCover, (0, self.listCoverY))
        return surface
    
    def getEvent(self,event):
        if event.type == pygame.constants.MOUSEBUTTONDOWN or event.type == pygame.constants.MOUSEMOTION:
            event.pos = (event.pos[0]-self.location[0],event.pos[1]-self.location[1])
        for child in self.childs:
            child.getEvent(event)


        if event.type == pygame.constants.MOUSEBUTTONDOWN:
            if event.button == pygame.constants.BUTTON_WHEELDOWN and self.index<=len(self.blocks)-5:
                self.index += 1
                for block in self.blocks:
                    block.location = (block.location[0],block.location[1]-150)
            if event.button == pygame.constants.BUTTON_WHEELUP and self.index>0:
                self.index -= 1
                for block in self.blocks:
                    block.location = (block.location[0],block.location[1]+150)
    
            

        

