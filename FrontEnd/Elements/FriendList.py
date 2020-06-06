from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Avatar import Avatar
from FrontEnd.Elements.CustomText import CustomText
from FrontEnd.Elements.RightClickMenu import RightClickMenu
from Common.base import readData
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
        self.avatar = self.createChild(Avatar, (25, 15), user['avatarURL'])
        self.nicknameText = self.createChild(CustomText, (120, 38), 'dengxian', 25, (0, 0, 0), user['nickname'])
        self.surface = FriendBlock.image
        self.location = location
        self.size = (350, 100)
        self.type = block_type
        self.doubleclick_start = False
        self.doubleclick_counter = 0

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] < x < self.location[0] + self.size[0] \
                and self.location[1] < y < self.location[1] + self.size[1]:
            return True
        return False

    def getEvent(self, event):
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
                self.state = 2
                self.surface = FriendBlock.image_onClick
                if self.doubleclick_start:
                    self.doubleclick_start = False
                    self.doubleclick_counter = 0
                    self.process.createSessionWindow(233)
                elif not self.doubleclick_start:
                    self.doubleclick_start = True

            else:
                self.state = 0
                self.surface = FriendBlock.image
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT and self.pos_in(event.pos):
            self.rightClickMenu.change_location(event.pos)
            self.rightClickMenu.set_user(self.user)
            self.rightClickMenu.enable()

    def update(self):
        if self.doubleclick_start:
            self.doubleclick_counter += 1
            if self.doubleclick_counter > 18:
                self.doubleclick_start = False
                self.doubleclick_counter = 0
        for child in self.childs:
            if child.active:
                child.update()

    def is_displayed(self):
        if -350 < self.location[0] < 350 and 0 <= self.location[1] <= 400:
            return True
        return False


class FriendList(Element):
    listCover = pygame.image.load('./resources/listCover.png')

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.surface = pygame.Surface((350, 500))
        self.surface.fill((255, 255, 255))
        self.size = (350, 500)
        self.friend_list = []
        self.group_list = []
        self.message_list = []
        self.blocks = []
        self.change_from = 0
        self.change_to = 0
        self.listCoverY = -200
        self.index = [0, 0, 0]
        self.frozen = False
        self.switch_counter = 0
        self.switch_speed = 0
        self.rightClickMenu = None
        self.refresh()

    def refresh(self):
        self.friend_list.clear()
        self.group_list.clear()
        self.message_list.clear()
        self.blocks.clear()
        self.childs.clear()
        self.rightClickMenu = self.createChild(RightClickMenu)
        data = readData(self.process.data)
        try:
            for i in range(len(data['messageList'])):
                user = data['messageList'][i]
                self.message_list.append(self.createChild(FriendBlock, (0, i * 100), user, 0, self.rightClickMenu))
                self.blocks.append(self.message_list[i])
            for i in range(len(data['friendList'])):
                user = data['friendList'][i]
                self.friend_list.append(self.createChild(FriendBlock, (350, i * 100), user, 1, self.rightClickMenu))
                self.blocks.append(self.friend_list[i])
            for i in range(len(data['groupList'])):
                user = data['groupList'][i]
                self.group_list.append(self.createChild(FriendBlock, (700, i * 100), user, 2, self.rightClickMenu))
                self.blocks.append(self.group_list[i])
        except KeyError:
            print('key error in FriendList')

    def display(self):
        surface = self.surface.copy()
        for block in self.blocks:
            if block.is_displayed():
                surface.blit(block.display(), block.location)
        if self.rightClickMenu.active:
            surface.blit(self.rightClickMenu.display(), self.rightClickMenu.location)
        if self.listCoverY < 500:
            surface.blit(FriendList.listCover, (0, self.listCoverY))
        return surface

    def getEvent(self, event):
        if not self.frozen:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.change_from == 0:
                    blocks_ = self.message_list
                    idx = 0
                elif self.change_from == 1:
                    blocks_ = self.friend_list
                    idx = 1
                elif self.change_from == 2:
                    blocks_ = self.group_list
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
                if block.is_displayed():
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

        if self.change_from != self.change_to:
            if self.change_from + 1 == self.change_to:
                self.switch_speed = -35
            elif self.change_from - 1 == self.change_to:
                self.switch_speed = 35
            elif self.change_from + 2 == self.change_to:
                self.switch_speed = -70
            elif self.change_from - 2 == self.change_to:
                self.switch_speed = 70
            if self.switch_counter < 10:
                self.switch_counter += 1
                for block in self.blocks:
                    block.location = (block.location[0] + self.switch_speed, block.location[1])
            else:
                self.change_from = self.change_to
                self.switch_counter = 0
        for child in self.childs:
            if child.active:
                child.update()
