from time import sleep

from FrontEnd.Elements.DropDownMenu import DropDownMenu
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.CustomText import CustomText
from FrontEnd.Elements.Image import Image
from Common.base import readData
import pygame
from FrontEnd.Elements.SelectButton import SelectButton


class GroupMemberList(Element):
    image = pygame.Surface((750, 650))
    image.fill((255, 255, 255))

    def __init__(self, process, location, groupShow):
        Element.__init__(self, process)
        self.location = location
        self.surface = GroupMemberList.image
        self.size = (750, 650)
        self.list_name = 'sessionMembers'
        self.group_show = groupShow
        self.session_members = groupShow['sessionMembers']
        self.manager_username = groupShow['managerUsername']
        self.index = 0

        self.refresh()

    def refresh(self):

        self.childs.clear()

        # 注意 在这之前要发一次14号/8号消息 目前不知道放到哪里去
        # 窗口刚打开时readData一次 这是深拷贝

        try:
            data = self.session_members

            n = len(data)
            for i in range(n):
                session_member = data[i]
                print(data[i])
                if session_member == self.manager_username:
                    self.createChild(GroupMemberBlock, (19, i * 40), session_member, 1)
                else:
                    self.createChild(GroupMemberBlock, (19, i * 40), session_member, 0)
        except KeyError:
            print('key error in FriendApplyList-ReceiverList')


    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        return surface

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_WHEELDOWN and self.index <= len(self.childs) - 5:
                self.index += 1
                for child in self.childs:
                    child.location = (child.location[0], child.location[1] - 140)
            if event.button == pygame.BUTTON_WHEELUP and self.index > 0:
                self.index -= 1
                for child in self.childs:
                    child.location = (child.location[0], child.location[1] + 140)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            if child.active:
                child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def update(self):
        for child in self.childs:
            if child.active:
                child.update()


class GroupMemberBlock(Element):
    # state==0 idle
    # state==1 hover
    # state==2 select
    image = pygame.image.load('./resources/GroupInforWindowUI/group_member_block.png')
    image_select = pygame.image.load('./resources/GroupInforWindowUI/group_member_block_select.png')
    #image.fill((255, 255, 255))
    # image_onHover = pygame.Surface((582, 40))
    # image_onHover.fill((245, 245, 245))
    # image_onClick = pygame.Surface((582, 40))
    # image_onClick.fill((240, 240, 240))
    # avatar_cover = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/news.png'), (75, 75))

    # isManager==1:是管理员
    def __init__(self, process, location, sessionMember, isManager):
        Element.__init__(self, process)
        self.applyBlock = sessionMember
        try:
            # # 头像
            # self.avatar = self.createChild(Image, (50, 30), (70, 70), receiverMessage['avatarAddress'])
            # self.receiver_username = self.createChild(CustomText, (30+90+30, 33), 'simhei', 26, (0, 0, 0), receiverMessage['receiverUsername'])
            # result = receiverMessage['result']
            # if(result == '1'):
            #     self.result = self.createChild(CustomText, (30+90+30,75), 'simhei', 18, (105,105,105), '已同意你的请求')
            # else:   # result == 0
            #     self.result = self.createChild(CustomText, (30+90+30, 75), 'simhei', 18, (105, 105, 105), '已拒绝你的请求')
            # self.receiver_time = self.createChild(CustomText, (750-200, 55), 'simhei', 16, (158, 158, 158), receiverMessage['time'])
            self.username = self.createChild(CustomText, (30,5),'simhei', 20, (55,55,55), sessionMember)
            if isManager == 1:
                self.manager = self.createChild(CustomText,(165,5),'simhei', 20, (55,55,55),'√')

        except KeyError:
            print('key error in GroupMemberBlock')
        self.surface = GroupMemberBlock.image
        self.location = location
        self.size = (582, 40)
        # 下面这几个都是zyx要用的
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

    # def pos_in_avatar(self, pos):
    #     x = pos[0]
    #     y = pos[1]
    #     if self.location[0] + 12 < x < self.location[0] + 12 + 75 \
    #             and self.location[1] + 12 < y < self.location[1] + 12 + 75:
    #         return True

    def getEvent(self, event):
        if self.is_displayed():
            if event.type == pygame.MOUSEMOTION:
                if self.state != 2:
                    if self.pos_in(event.pos):
                        self.state = 1
                        self.surface = GroupMemberBlock.image_select  ###
                        # self.surface = FriendApplyBlock.image_onHover
                    else:
                        self.state = 0
                        self.surface = GroupMemberBlock.image
                # if self.pos_in_avatar(event.pos):
                #     self.covered = True
                # else:
                #     self.covered = False
                return
            # if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            #     if self.pos_in(event.pos):
            #         self.state = 2
            #         self.surface = ReceiverBlock.image ###
            #         # self.surface = FriendApplyBlock.image_onClick
            #         if self.pos_in_avatar(event.pos):
            #             print('查看' + self.user['nickname'] + '资料')
            #             # self.process.createxxxxxx
            #         else:
            #             if self.doubleclick_start:
            #                 self.doubleclick_start = False
            #                 self.doubleclick_counter = 0
            #                 self.process.createSessionWindow(233)
            #             elif not self.doubleclick_start:
            #                 self.doubleclick_start = True
            #     else:
            #         self.state = 0
            #         self.surface = ReceiverBlock.image

    def update(self):
        if self.is_displayed():
        #     if self.doubleclick_start:
        #         self.doubleclick_counter += 1
        #         if self.doubleclick_counter > 18:
        #             self.doubleclick_start = False
        #             self.doubleclick_counter = 0
            for child in self.childs:
                if child.active:
                    child.update()

    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        # if self.covered:
        #     surface.blit(FriendApplyBlock.avatar_cover, (12, 12))
        return surface

    def is_displayed(self):
        if 0 <= self.location[1] <= 800:   # 800让最下面的框可以选中 也就是大于窗口的高度
            return True
        return False

    # def update_info(self, user):
    #     try:
    #         self.avatar = self.createChild(Image, (12, 12), (75, 75), user['avatarURL'])
    #         self.receiver_username.set_text(user['nickname'])
    #         self.last_message.set_text('最最最最最最最新消息')
    #         self.receiver_time.set_text('23:33')
    #     except KeyError:
    #         print('key error in update FriendBlock')

