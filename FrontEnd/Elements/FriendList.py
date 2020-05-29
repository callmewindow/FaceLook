from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Avatar import Avatar
from FrontEnd.Elements.text_default import text_default
from FrontEnd.Elements.RightClickMenu import RightClickMenu
import pygame


class FriendBlock(Element):
    # state==0 idle
    # state==1 hover
    # state==2 select
    # type==0 message
    # type==1 friend
    # type==2 group
    image = pygame.Surface((350, 100))
    image.fill((255, 255, 255))
    image_onHover = pygame.Surface((350, 100))
    image_onHover.fill((245, 245, 245))
    image_onClick = pygame.Surface((350, 100))
    image_onClick.fill((240, 240, 240))

    def __init__(self, process, location, user, block_type, menu):
        Element.__init__(self, process)
        self.user = user
        self.rightClickMenu = menu
        self.avatar = self.createChild(Avatar, (25, 15), user.avatarURL)
        user_state_text = ' (online)' if user.state == 1 else ' (offline)'
        self.nicknameText = self.createChild(text_default, (120, 38), user.nickname + user_state_text, (0, 0, 0))
        self.surface = FriendBlock.image
        self.location = location
        self.size = (350, 100)
        self.type = block_type

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] <= x <= self.location[0] + self.size[0] \
                and self.location[1] <= y <= self.location[1] + self.size[1]:
            return True
        return False

    def getEvent(self, event):
        if 0 <= self.location[1] <= 400:
            if event.type == pygame.MOUSEMOTION and self.state != 2:
                if self.pos_in(event.pos):
                    self.state = 1
                    self.surface = FriendBlock.image_onHover
                else:
                    self.state = 0
                    self.surface = FriendBlock.image
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if self.pos_in(event.pos):
                    print(self.user.nickname)
                    if self.state == 2:
                        self.process.createSessionWindow(233)
                    else:
                        self.state = 2
                        self.surface = FriendBlock.image_onClick
                else:
                    self.state = 0
                    self.surface = FriendBlock.image
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT and self.pos_in(event.pos):
                self.rightClickMenu.change_location(event.pos)
                self.rightClickMenu.set_user(self.user)
                self.rightClickMenu.enable()


class FriendList(Element):
    listCover = pygame.image.load('./resources/listCover.png')

    def __init__(self, process, location, friend_list, group_list, message_list):
        Element.__init__(self, process)
        self.location = location
        self.surface = pygame.Surface((350, 500))
        self.surface.fill((220, 220, 220))
        self.size = (350, 500)
        self.friendList = []
        self.groupList = []
        self.messageList = []
        self.blocks = []
        self.has_changed = False
        self.change_to = 0
        self.listCoverY = -200
        self.cover = FriendList.listCover
        self.rightClickMenu = self.createChild(RightClickMenu)
        self.index = [0, 0, 0]
        self.frozen = False

        for i in range(len(friend_list)):
            user = friend_list[i]
            self.friendList.append(self.createChild(FriendBlock, (0, i * 100), user, 1, self.rightClickMenu))
            self.blocks.append(self.friendList[i])
        for i in range(len(group_list)):
            user = group_list[i]
            self.groupList.append(self.createChild(FriendBlock, (0, i * 100), user, 2, self.rightClickMenu))
            self.blocks.append(self.groupList[i])
        for i in range(len(message_list)):
            user = message_list[i]
            self.messageList.append(self.createChild(FriendBlock, (0, i * 100), user, 0, self.rightClickMenu))
            self.blocks.append(self.messageList[i])

    def display(self):
        surface = self.surface.copy()
        for block in self.blocks:
            if block.active:
                surface.blit(block.display(), block.location)
        if self.rightClickMenu.active:
            surface.blit(self.rightClickMenu.display(), self.rightClickMenu.location)
        if self.listCoverY < 500:
            surface.blit(self.cover, (0, self.listCoverY))
        return surface

    def getEvent(self, event):
        if not self.frozen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.change_to == 0:
                    blocks_ = self.messageList
                    idx = 0
                elif self.change_to == 1:
                    blocks_ = self.friendList
                    idx = 1
                elif self.change_to == 2:
                    blocks_ = self.groupList
                    idx = 2
                if event.button == pygame.BUTTON_WHEELDOWN and self.index[idx] <= len(blocks_) - 6:
                    self.index[idx] += 1
                    for block in blocks_:
                        block.location = (block.location[0], block.location[1] - 100)
                if event.button == pygame.BUTTON_WHEELUP and self.index[idx] > 0:
                    self.index[idx] -= 1
                    for block in blocks_:
                        block.location = (block.location[0], block.location[1] + 100)

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])

        if not self.frozen:
            for block in self.blocks:
                if block.active:
                    block.getEvent(event)
        if self.rightClickMenu.active:
            self.rightClickMenu.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def update(self):
        if self.listCoverY < 500:
            self.listCoverY = self.listCoverY + 8
        if self.rightClickMenu.active:
            self.frozen = True
        if self.rightClickMenu.has_closed:
            self.frozen = False
            self.rightClickMenu.has_closed = False
        if self.has_changed:
            for block in self.blocks:
                if block.type != self.change_to:
                    block.disable()
                else:
                    block.enable()
        for child in self.childs:
            if child.active:
                child.update()

