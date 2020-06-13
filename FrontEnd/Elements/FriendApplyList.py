from time import sleep

from FrontEnd.Elements.DropDownMenu import DropDownMenu
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.CustomText import CustomText
from FrontEnd.Elements.Image import Image
from Common.base import readData
import pygame
from FrontEnd.Elements.SelectButton import SelectButton


class ReceiverList(Element):
    image = pygame.Surface((750, 650))
    image.fill((255, 255, 255))

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.surface = ReceiverList.image
        self.size = (750, 650)

        self.index = 0
        self.list_name = 'receiverList'
        self.refresh()

    def refresh(self):

        self.childs.clear()

        # 注意 在这之前要发一次14号/8号消息 目前不知道放到哪里去
        # 窗口刚打开时readData一次 这是深拷贝

        try:
            data = readData(self.process.data)

            n = len(data[self.list_name])
            for i in range(len(data[self.list_name])):
                receiverMessage = data[self.list_name][n-1-i]
                self.createChild(ReceiverBlock, (0, i * 130), receiverMessage)
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


class ReceiverBlock(Element):
    # state==0 idle
    # state==1 hover
    # state==2 select
    image = pygame.image.load('./resources/FriendApplyWindowUI/applyblock_bg.png')
    image_select = pygame.image.load('./resources/FriendApplyWindowUI/applyblock_bg_select.png')
    #image.fill((255, 255, 255))
    image_onHover = pygame.Surface((750, 130))
    image_onHover.fill((245, 245, 245))
    image_onClick = pygame.Surface((750, 130))
    image_onClick.fill((240, 240, 240))
    avatar_cover = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/news.png'), (75, 75))

    def __init__(self, process, location, receiverMessage):
        Element.__init__(self, process)
        self.applyBlock = receiverMessage
        try:
            # 头像
            self.avatar = self.createChild(Image, (50, 30), (70, 70), receiverMessage['avatarAddress'])
            self.receiver_username = self.createChild(CustomText, (30+90+30, 33), 'simhei', 26, (0, 0, 0), receiverMessage['receiverUsername'])
            result = receiverMessage['result']
            if(result == '1'):
                self.result = self.createChild(CustomText, (30+90+30,75), 'simhei', 18, (105,105,105), '已同意你的请求')
            else:   # result == 0
                self.result = self.createChild(CustomText, (30+90+30, 75), 'simhei', 18, (105, 105, 105), '已拒绝你的请求')
            self.receiver_time = self.createChild(CustomText, (750-200, 55), 'simhei', 16, (158, 158, 158), receiverMessage['time'])
        except KeyError:
            print('key error in ReceiverBlock')
        self.surface = ReceiverBlock.image
        self.location = location
        self.size = (750, 130)
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
                        self.surface = ReceiverBlock.image_select  ###
                        # self.surface = FriendApplyBlock.image_onHover
                    else:
                        self.state = 0
                        self.surface = ReceiverBlock.image
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


#####################################################分割线#######################################################

class RequestorList(Element):
    image = pygame.Surface((750, 650))
    image.fill((255, 255, 255))

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.surface = RequestorList.image
        self.size = (750, 650)

        self.index = 0
        self.list_name = 'requestorList'
        self.refresh()

    def refresh(self):

        self.childs.clear()

        # 注意 在这之前要发一次14号/8号消息 目前不知道放到哪里去
        # 窗口刚打开时readData一次 这是深拷贝

        try:
            data = readData(self.process.data)

            n = len(data[self.list_name])
            for i in range(len(data[self.list_name])):
                requestorMessage = data[self.list_name][n-1-i]
                self.createChild(RequestorBlock, (0, i * 130), requestorMessage)
        except KeyError:
            print('key error in FriendApplyList-RequestorList')

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


class RequestorBlock(Element):


    # state==0 idle
    # state==1 hover
    # state==2 select
    image = pygame.image.load('./resources/FriendApplyWindowUI/applyblock_bg.png')
    image_select = pygame.image.load('./resources/FriendApplyWindowUI/applyblock_bg_select.png')
    #image.fill((255, 255, 255))
    image_onHover = pygame.Surface((750, 130))
    image_onHover.fill((245, 245, 245))
    image_onClick = pygame.Surface((750, 130))
    image_onClick.fill((240, 240, 240))
    avatar_cover = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/news.png'), (75, 75))

    def __init__(self, process, location, requestorMessage):
        Element.__init__(self, process)
        self.applyBlock = requestorMessage
        try:
            # 头像
            self.avatar = self.createChild(Image, (50, 30), (70, 70), requestorMessage['avatarAddress'])
            self.requestor_username = self.createChild(CustomText, (30 + 90 + 30, 33), 'simhei', 26, (0, 0, 0), requestorMessage['requestorUsername'])
            if requestorMessage['checkMessage']:
                self.check_message = self.createChild(CustomText, (30 + 90 + 30, 75), 'simhei', 18, (105, 105, 105), '验证消息：' + requestorMessage['checkMessage'])
            else:  # 没写验证信息 默认填“申请加我为好友”
                self.check_message = self.createChild(CustomText, (30 + 90 + 30, 75), 'simhei', 18, (105, 105, 105),'验证消息：申请加我为好友')

           # self.result_menu = self.createChild(DropDownMenu, (750 - 205, 37), ['未处理', '同意', '拒绝'])

            self.result_agree = self.createChild(SelectButton, (750 - 200 - 10, 37), '同意', (12, 5))
            self.result_disagree = self.createChild(SelectButton, (750 - 200+50+10, 37), '拒绝', (12, 5))
            self.result_agree_select = self.createChild(CustomText, (750 - 200 + 50, 37), 'simhei', 20, (158, 158, 158),'已同意')
            self.result_disagree_select = self.createChild(CustomText, (750 - 200 + 50, 37), 'simhei', 20, (158, 158, 158),'已拒绝')
            self.result_agree_select.disable()
            self.result_disagree_select.disable()
           # self.result_agree.disable()
         #   self.result_agree = self.createChild(CustomText, (750 - 205+50, 57), 'simhei', 16, (158, 158, 158), '拒绝')
            self.requestor_time = self.createChild(CustomText, (750 - 200, 77), 'simhei', 16, (158, 158, 158), requestorMessage['time'])
        except KeyError:
            print('key error in FriendBlock')
        self.surface = RequestorBlock.image
        self.location = location
        self.size = (750, 130)
        self.is_replied = False
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

    def pos_in_dropdownmenu(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0]+750-205 < x < self.location[0]+750-205 + 120 \
                and self.location[1] + 37 < y < self.location[1] + 37 + 31:
            return True

    def getEvent(self, event):
        if self.is_displayed():
            # zyx add start
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
            for child in self.childs:
                if child.active:
                    child.getEvent(event)
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])
            # zyx add end

            if event.type == pygame.MOUSEMOTION:
                if self.state != 2:
                    if self.pos_in(event.pos):
                        self.state = 1
                        self.surface = RequestorBlock.image_select  ###
                        # self.surface = FriendApplyBlock.image_onHover
                    else:
                        self.state = 0
                        self.surface = RequestorBlock.image
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if self.pos_in(event.pos):
                    if self.result_agree.isClick and self.is_replied == False:
                        print('send request with agree')
                        request = {
                            'messageNumber': '12',
                            'requestorUsername':self.applyBlock['requestorUsername'],
                            'result':'1',
                        }
                        self.process.requestQueue.put(request)
                        print(request)

                        # zyx need
                        request = {
                            'messageNumber': '6',
                            'sessionName':None,
                        }
                        self.process.requestQueue.put(request)
                        print(request)

                        self.is_replied = True
                        sleep(0.1)
                        self.result_agree.disable()
                        self.result_disagree.disable()
                        self.result_agree_select.enable()
                    elif self.result_disagree.isClick and self.is_replied == False:
                        print('send request with disagree')
                        request = {
                            'messageNumber': '12',
                            'requestorUsername':self.applyBlock['requestorUsername'],
                            'result':'0',
                        }
                        self.process.requestQueue.put(request)
                        print(request)

                        self.is_replied = True
                        sleep(0.1)
                        self.result_agree.disable()
                        self.result_disagree.disable()
                        self.result_disagree_select.enable()
                    # self.state = 2
                    # self.surface = RequestorBlock.image_select ###
                    # if self.pos_in_dropdownmenu(event.pos):
                    #     print('dropdownmenu')
                    #     print(event.pos)
                    # if self.is_replied == False:
                    #         key = self.result_menu.get_selected()
                    #         if key == '同意':
                    #             print('send request with agree')
                    #             # request = {
                    #             #     'messageNumber': '12',
                    #             #     'requestorUsername':'zmxtest',
                    #             #     'result':'1',
                    #             # }
                    #             # self.process.requestQueue.put(request)
                    #         else:
                    #             print('send request with disagree')
                    #             # request = {
                    #             #     'messageNumber': '12',
                    #             #     'requestorUsername': '',
                    #             #     'result': '0',
                    #             # }
                    #             # self.process.requestQueue.put(request)
                    #         self.is_replied = True
                else:
                    self.state = 0
                    self.surface = RequestorBlock.image

    # zyx add
    # def getEvent(self, event):
    #     if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
    #         event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
    #     for child in self.childs:
    #         if child.active:
    #             child.getEvent(event)
    #     if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
    #         event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def update(self):
        if self.is_displayed():
            # if self.doubleclick_start:
            #     self.doubleclick_counter += 1
            #     if self.doubleclick_counter > 18:
            #         self.doubleclick_start = False
            #         self.doubleclick_counter = 0
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
        if 0 <= self.location[1] <= 800:
            return True
        return False

    # def update_info(self, user):
    #     try:
    #         self.avatar = self.createChild(Image, (12, 12), (75, 75), user['avatarURL'])
    #         self.requestor_username.set_text(user['nickname'])
    #         self.last_message.set_text('最最最最最最最新消息')
    #         self.requestor_time.set_text('23:33')
    #     except KeyError:
    #         print('key error in update FriendBlock')



