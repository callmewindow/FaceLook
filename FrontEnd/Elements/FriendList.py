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
            self.avatar = self.createChild(Image, (12, 12), (75, 75), user['avatarAddress'])
            self.nickname = self.createChild(CustomText, (100, 24), 'dengxian', 22, (0, 0, 0), user['nickname'])
            mes = self.process.bet.localStorage.get_friend_last_message(user['username'])
            self.last_message = self.createChild(CustomText, (100, 60), 'dengxian', 16, (128, 128, 128),
                                                 ' 暂无消息' if mes is None else mes['content'])
            self.last_date = self.createChild(CustomText, (300, 40), 'dengxian', 16, (128, 128, 128),
                                              ' ' if mes is None else mes['time'][5:10])
            self.last_time = self.createChild(CustomText, (302, 60), 'dengxian', 16, (128, 128, 128),
                                              ' ' if mes is None else mes['time'][11:13] + ':' + mes['time'][14:16])
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
                        self.process.requestQueue.put({'messageNumber': '4'})
                        self.process.createInfoWindow(self.user)
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

    def update_info(self):
        try:
            mes = self.process.bet.localStorage.get_friend_last_message(self.user['username'])
            self.last_message.set_text(' 暂无消息' if mes is None else mes['content'])
            self.last_date.set_text(' ' if mes is None else mes['time'][5:10])
            self.last_time.set_text(' ' if mes is None else mes['time'][11:13] + ':' + mes['time'][14:16])
        except KeyError:
            print('key error in update FriendBlock')


class GroupBlock(Element):
    # state==0 idle
    # state==1 hover
    # state==2 select
    image = pygame.Surface((350, 100))
    image.fill((255, 255, 255))
    image_onHover = pygame.Surface((350, 100))
    image_onHover.fill((245, 245, 245))
    image_onClick = pygame.Surface((350, 100))
    image_onClick.fill((240, 240, 240))

    # group = {'sessionID': '', 'sessionName': ''}
    def __init__(self, process, location, group):
        Element.__init__(self, process)
        self.group = group
        try:
            self.nickname = self.createChild(CustomText, (25, 24), 'dengxian', 22, (0, 0, 0), group['sessionName'])
            mes = self.process.bet.localStorage.get_session_last_message(group['sessionID'])
            self.last_message = self.createChild(CustomText, (25, 60), 'dengxian', 16, (128, 128, 128),
                                                 ' 暂无消息' if mes is None else mes['content'])
            self.last_date = self.createChild(CustomText, (300, 40), 'dengxian', 16, (128, 128, 128),
                                              ' ' if mes is None else mes['time'][5:10])
            self.last_time = self.createChild(CustomText, (302, 60), 'dengxian', 16, (128, 128, 128),
                                              ' ' if mes is None else mes['time'][11:13] + ':' + mes['time'][14:16])
        except KeyError:
            print('key error in GroupBlock')
        self.surface = GroupBlock.image
        self.location = location
        self.size = (350, 100)
        self.doubleclick_start = False
        self.doubleclick_counter = 0
        self.state = 0

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] < x < self.location[0] + self.size[0] \
                and self.location[1] < y < self.location[1] + self.size[1]:
            return True
        return False

    def getEvent(self, event):
        if self.is_displayed():
            if event.type == pygame.MOUSEMOTION:
                if self.state != 2:
                    if self.pos_in(event.pos):
                        self.state = 1
                        self.surface = GroupBlock.image_onHover
                    else:
                        self.state = 0
                        self.surface = GroupBlock.image
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if self.pos_in(event.pos):
                    self.state = 2
                    self.surface = GroupBlock.image_onClick
                    if self.doubleclick_start:
                        self.doubleclick_start = False
                        self.doubleclick_counter = 0
                        self.process.createSessionWindow(233)
                    elif not self.doubleclick_start:
                        self.doubleclick_start = True
                else:
                    self.state = 0
                    self.surface = GroupBlock.image

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

    def is_displayed(self):
        if 0 <= self.location[1] <= 400:
            return True
        return False

    def update_info(self):
        try:
            for i in self.process.bet.localStorage.get_groups():
                if i['sessionID'] == self.group['sessionID']:
                    self.nickname.set_text(i['sessionName'])
            mes = self.process.bet.localStorage.get_session_last_message(self.group['sessionID'])
            self.last_message.set_text(' 暂无消息' if mes is None else mes['content'])
            self.last_date.set_text(' ' if mes is None else mes['time'][5:10])
            self.last_time.set_text(' ' if mes is None else mes['time'][11:13] + ':' + mes['time'][14:16])
        except KeyError:
            print('key error in update GroupBlock')


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
        self.type_ = type_
        self.frozen = False
        self.sort_counter = 0
        self.refresh()

    def refresh(self):
        self.childs.clear()
        data = readData(self.process.data)
        try:
            if self.type_ == 0:
                for i in range(len(data['friendList'])):
                    user = data['friendList'][i]
                    self.createChild(FriendBlock, (0, i * 100), user)
            else:
                group_list = self.process.bet.localStorage.get_groups()
                for i in range(len(group_list)):
                    group = group_list[i]
                    self.createChild(GroupBlock, (0, i * 100), group)
        except KeyError:
            print('key error in FriendList')

    def update_info(self):
        for child in self.childs:
            child.update_info()

    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        if self.type_ == 0 and self.listCoverY < 500:
            surface.blit(FriendList.listCover, (0, self.listCoverY))
        return surface

    def getEvent(self, event):
        if not self.frozen:
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
        if self.type_ == 0 and self.listCoverY < 500:
            self.listCoverY = self.listCoverY + 8
        for child in self.childs:
            if child.active:
                child.update()
