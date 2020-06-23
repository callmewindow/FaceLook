from time import sleep
from FrontEnd.Elements.DropDownMenu import DropDownMenu
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.CustomText import CustomText
from FrontEnd.Elements.Image import Image
from FrontEnd.Elements.SelectButton import SelectButton
from FrontEnd.Elements.GroupInforButton import GroupInforButton
from FrontEnd.Elements.TextButton import TextButton
from Common.dataFunction import *
import pygame


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
        self.session_members = self.group_show['sessionMembers']
        self.manager_username = self.group_show['managerUsername']
        self.index = 0

        self.refresh()

    def refresh(self):
        self.childs.clear()

        try:
            self.session_members = self.group_show['sessionMembers']
            self.manager_username = self.group_show['managerUsername']
            data = readData(self.process.data)
            self.sessionVer = data['sessionList']['version']
            users = data['usernameResult']['list']
            n = len(self.session_members)
            for i in range(n):
                session_member = self.session_members[i]
                tempUser = {}
                for user in users:
                    if session_member == user['username']:
                        tempUser = user
                if session_member == self.manager_username:
                    self.createChild(GroupMemberBlock, (19, i * 40), session_member, 1, tempUser)
                else:
                    self.createChild(GroupMemberBlock, (19, i * 40), session_member, 0, tempUser)
        except KeyError:
            print('key error in GroupMemberList')

    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        return surface

    def getEvent(self, event):
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
        self.counter = (self.counter+1)%60
        if self.counter < 59: return
        else:
            data = readData(self.process.data)
            # 定时更新session信息
            if data['sessionList']['version'] > self.sessionVer:
                self.sessionVer = data['sessionList']['version']
                allSession = data['sessionList']['list']
                # 获取完整session
                sessionId = self.group_show['sessionId']
                for session in allSession:
                    if session['sessionId'] == sessionId:
                        self.group_show = session
                        break
                self.refresh()


class GroupMemberBlock(Element):
    image = pygame.image.load('./resources/GroupInforWindowUI/group_member_block.png')
    image_select = pygame.image.load('./resources/GroupInforWindowUI/group_member_block_select.png')

    # isManager==1:是管理员
    def __init__(self, process, location, sessionMember, isManager, userShow):
        Element.__init__(self, process)
        self.applyBlock = sessionMember
        try:
            self.username = self.createChild(CustomText, (30,5),'simhei', 20, (55,55,55), sessionMember)
            if isManager == 1:
                self.manager = self.createChild(CustomText,(165,5),'simhei', 20, (55,55,55),'√')
        except KeyError:
            print('key error in GroupMemberBlock')
        
        data = readData(self.process.data)
        self.username = data['user']['username']

        self.userShow = userShow
        self.usernameShow = sessionMember
        self.surface = GroupMemberBlock.image
        self.location = location
        self.size = (582, 40)

        self.lookButton = self.createChild(TextButton, (280, 2), "查看信息", 16, (80, 30))
        self.outButton = self.createChild(GroupInforButton,(380,2),'踢出群聊',(10,5),16,(80,30),
                                           './resources/GroupInforWindowUI/quit_button_hover.png',
                                           './resources/GroupInforWindowUI/quit_button.png',
                                           './resources/GroupInforWindowUI/quit_button_hover.png')
        if self.username != self.process.groupShow['managerUsername']:
            self.outButton.disable()

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] < x < self.location[0] + self.size[0] \
                and self.location[1] < y < self.location[1] + self.size[1]:
            return True
        return False

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            if child.active:
                child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

        if self.lookButton.state == 2:
            self.lookButton.setState(0)
            self.process.createUserInforWindow(self.userShow)
        
        if self.outButton.state == 2:
            self.outButton.setState(0)
            request = {
                'messageNumber': '22',
                'username': self.usernameShow,
                'sessionId': self.process.groupShow['sessionId'],
            }
            print(request)
            # self.process.requestQueue.put(request)

    def update(self):
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