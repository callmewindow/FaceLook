from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.CustomText import CustomText
from FrontEnd.Elements.Image import Image
from Common.base import readData
import pygame


class FriendBlock(Element):
    # state==0 idle
    # state==1 hover
    # state==2 select
    image = pygame.Surface((350, 100))
    image.fill((255, 255, 255))
    image_onHover = pygame.Surface((350, 100))
    image_onHover.fill((245, 245, 245))
    image_onClick = pygame.Surface((350, 100))
    image_onClick.fill((240, 240, 240))
    avatar_cover = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/news.png'), (75, 75))

    def __init__(self, process, location, user):
        Element.__init__(self, process)
        self.user = user
        try:
            self.avatar = self.createChild(Image, (12, 12), (75, 75), user['avatarURL'])
            self.nickname = self.createChild(CustomText, (100, 24), 'dengxian', 22, (0, 0, 0), user['nickname'])
            self.last_message = self.createChild(CustomText, (100, 60), 'dengxian', 16, (128, 128, 128), '最最最最最最最新消息')
            self.last_time = self.createChild(CustomText, (300, 60), 'dengxian', 16, (128, 128, 128), '23:33')
        except KeyError:
            print('key error in FriendBlock')
        self.surface = FriendBlock.image
        self.location = location
        self.size = (350, 100)
        self.doubleclick_start = False
        self.doubleclick_counter = 0
        self.state = 0
        self.covered = False

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] < x < self.location[0] + self.size[0] \
                and self.location[1] < y < self.location[1] + self.size[1]:
            return True
        return False

    def pos_in_avatar(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] + 12 < x < self.location[0] + 12 + 75 \
                and self.location[1] + 12 < y < self.location[1] + 12 + 75:
            return True

    def getEvent(self, event):
        if self.is_displayed():
            if event.type == pygame.MOUSEMOTION:
                if self.state != 2:
                    if self.pos_in(event.pos):
                        self.state = 1
                        self.surface = FriendBlock.image_onHover
                    else:
                        self.state = 0
                        self.surface = FriendBlock.image
                if self.pos_in_avatar(event.pos):
                    self.covered = True
                else:
                    self.covered = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if self.pos_in(event.pos):
                    self.state = 2
                    self.surface = FriendBlock.image_onClick
                    if self.pos_in_avatar(event.pos):
                        print('查看' + self.user['nickname'] + '资料')
                        # self.process.createxxxxxx
                    else:
                        if self.doubleclick_start:
                            self.doubleclick_start = False
                            self.doubleclick_counter = 0
                            self.process.createSessionWindow(233)
                        elif not self.doubleclick_start:
                            self.doubleclick_start = True
                else:
                    self.state = 0
                    self.surface = FriendBlock.image

    def update(self):
        if self.is_displayed():
            if self.doubleclick_start:
                self.doubleclick_counter += 1
                if self.doubleclick_counter > 18:
                    self.doubleclick_start = False
                    self.doubleclick_counter = 0
            for child in self.childs:
                if child.active:
                    child.update()

    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        if self.covered:
            surface.blit(FriendBlock.avatar_cover, (12, 12))
        return surface

    def is_displayed(self):
        if 0 <= self.location[1] <= 400:
            return True
        return False

    def update_info(self, user):
        try:
            self.avatar = self.createChild(Image, (12, 12), (75, 75), user['avatarURL'])
            self.nickname.set_text(user['nickname'])
            self.last_message.set_text('最最最最最最最新消息')
            self.last_time.set_text('23:33')
        except KeyError:
            print('key error in update FriendBlock')


class FriendList(Element):
    # type_ == 0 好友
    # type_ == 1 群组
    listCover = pygame.image.load('./resources/listCover.png')
    image = pygame.Surface((350, 500))
    image.fill((255, 255, 255))

    def __init__(self, process, location, type_):
        Element.__init__(self, process)
        self.location = location
        self.surface = FriendList.image
        self.size = (350, 500)
        self.listCoverY = -200
        self.index = 0
        self.list_name = 'friendList' if type_ == 0 else 'groupList'
        self.refresh()

    def refresh(self):
        self.childs.clear()
        data = readData(self.process.data)
        try:
            for i in range(len(data[self.list_name])):
                user = data[self.list_name][i]
                self.createChild(FriendBlock, (0, i * 100), user)
        except KeyError:
            print('key error in FriendList')

    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        if self.list_name == 'friendList' and self.listCoverY < 500:
            surface.blit(FriendList.listCover, (0, self.listCoverY))
        return surface

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_WHEELDOWN and self.index <= len(self.childs) - 6:
                self.index += 1
                for child in self.childs:
                    child.location = (child.location[0], child.location[1] - 100)
            if event.button == pygame.BUTTON_WHEELUP and self.index > 0:
                self.index -= 1
                for child in self.childs:
                    child.location = (child.location[0], child.location[1] + 100)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            if child.active:
                child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def update(self):
        if self.list_name == 'friendList' and self.listCoverY < 500:
            self.listCoverY = self.listCoverY + 8
        for child in self.childs:
            if child.active:
                child.update()
