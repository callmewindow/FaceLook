from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.CustomText import CustomText
from FrontEnd.Elements.Avatar import Avatar
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
    avatar_cover = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/news.png'), (60, 60))

    def __init__(self, process, location, user):
        Element.__init__(self, process)
        self.user = user
        try:
            self.avatar = self.createChild(Avatar, (20, 20), (60, 60), user['avatarAddress'])
            self.nickname = self.createChild(CustomText, (100, 20), 'simhei', 20, (0, 0, 0), user['nickname'], 190)
            self.last_message = self.createChild(CustomText, (100, 56), 'simhei', 18, (128, 128, 128), '暂无消息' if user['latestMessage']['content'] == '' else user['latestMessage']['content'], 190)
            self.last_date = self.createChild(CustomText, (300, 40), 'simhei', 16, (128, 128, 128), ' ' if user['latestMessage']['time'] == '' else user['latestMessage']['time'][5:10])
            self.last_time = self.createChild(CustomText, (300, 60), 'simhei', 16, (128, 128, 128), ' ' if user['latestMessage']['time'] == '' else user['latestMessage']['time'][11:13] + ':' + user['latestMessage']['time'][14:16])
            self.compared_time = '0' if user['latestMessage']['time'] == '' else user['latestMessage']['time']
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
        if self.location[0] + 20 < x < self.location[0] + 20 + 60 \
                and self.location[1] + 20 < y < self.location[1] + 20 + 60:
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
            surface.blit(FriendBlock.avatar_cover, (20, 20))
        return surface

    def is_displayed(self):
        if 0 <= self.location[1] <= 400:
            return True
        return False

    '''def update_info(self):
        try:
            mes = self.process.bet.localStorage.get_friend_last_message(self.user['username'])
            self.last_message.set_text(' 暂无消息' if mes is None else mes['content'])
            self.last_date.set_text(' ' if mes is None else mes['time'][5:10])
            self.last_time.set_text(' ' if mes is None else mes['time'][11:13] + ':' + mes['time'][14:16])
        except KeyError:
            print('key error in update FriendBlock')'''


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
            self.nickname = self.createChild(CustomText, (25, 24), 'simhei', 20, (0, 0, 0), group['sessionName'], 260)
            self.last_message = self.createChild(CustomText, (25, 56), 'simhei', 18, (128, 128, 128), '暂无消息' if group['latestMessage']['content'] == '' else group['latestMessage']['content'], 260)
            self.last_date = self.createChild(CustomText, (300, 40), 'simhei', 16, (128, 128, 128), ' ' if group['latestMessage']['time'] == '' else group['latestMessage']['time'][5:10])
            self.last_time = self.createChild(CustomText, (300, 60), 'simhei', 16, (128, 128, 128), ' ' if group['latestMessage']['time'] == '' else group['latestMessage']['time'][11:13] + ':' + group['latestMessage']['time'][14:16])
            self.compared_time = '0' if group['latestMessage']['time'] == '' else group['latestMessage']['time']
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

    '''def update_info(self):
        try:
            for i in self.process.bet.localStorage.get_groups():
                if i['sessionID'] == self.group['sessionID']:
                    self.nickname.set_text(i['sessionName'])
            mes = self.process.bet.localStorage.get_session_last_message(self.group['sessionID'])
            self.last_message.set_text(' 暂无消息' if mes is None else mes['content'])
            self.last_date.set_text(' ' if mes is None else mes['time'][5:10])
            self.last_time.set_text(' ' if mes is None else mes['time'][11:13] + ':' + mes['time'][14:16])
        except KeyError:
            print('key error in update GroupBlock')'''


class FriendList(Element):
    # type_ == 0 好友
    # type_ == 1 群组
    listCover = pygame.image.load('./resources/listCover.png')
    image = pygame.Surface((350, 500))
    image.fill((255, 255, 255))

    def __init__(self, process, location, type_, list_):
        Element.__init__(self, process)
        self.location = location
        self.surface = FriendList.image
        self.size = (350, 500)
        self.listCoverY = -200
        self.index = 0
        self.type_ = type_
        self.frozen = False
        self.sort_counter = 0
        self.refresh(list_)

    def refresh(self, list_):
        base = 0 if len(self.childs) == 0 else self.childs[0].location[1]
        self.childs.clear()
        len_ = len(list_)
        try:
            for i in range(len_):
                user = list_[i]
                if self.type_ == 0:
                    self.createChild(FriendBlock, (0, i * 100 + base), user)
                else:
                    self.createChild(GroupBlock, (0, i * 100 + base), user)
        except KeyError:
            print('key error in FriendList')
        for i in range(len_ - 1):
            for j in range(len_ - i - 1):
                if self.childs[j].compared_time < self.childs[j + 1].compared_time:
                    self.childs[j].location, self.childs[j + 1].location = self.childs[j + 1].location, self.childs[j].location
                    self.childs[j], self.childs[j + 1] = self.childs[j + 1], self.childs[j]

    '''def update_info(self):
        for child in self.childs:
            child.update_info()'''

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
