from time import sleep
import pygame
from Common.base import *
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.GroupInforButton import GroupInforButton
from FrontEnd.Elements.GroupMemberList import GroupMemberList
from FrontEnd.Elements.PicButton import PicButton
from FrontEnd.Elements.SelfInfo import SelfInfo
from FrontEnd.Elements.text_variable import text_variable
from FrontEnd.Elements.InforBar import InforBar
from FrontEnd.Elements.ModifyBar import ModifyBar
from FrontEnd.Elements.TripleStateButton import TripleStateButton
from FrontEnd.Elements.TextButton import TextButton
from FrontEnd.Elements.Image import Image
from FrontEnd.Elements.Button import UserCloseButton, CloseButton, MinimizeButton, UserMinimizeButton, \
    GrayMinimizeButton, GrayCloseButton
from FrontEnd.Elements.SingleInputBox import InputBox
from FrontEnd.Elements.AddCheckMessage import AddCheckMessage
from FrontEnd.Elements.Alert import Alert
from Common.dataFunction import *

class GroupInforWindowBackground(Element):
    # state == 0 群主
    # state == 1 群成员

    image_left = pygame.Surface((300,720))
    image_left.fill((238,99,149))

    def __init__(self, process):
        Element.__init__(self, process)
        self.groupShow = self.process.groupShow  # 数据传入
        data = readData(self.process.data)
        self.username = data['user']['username']
        if self.groupShow['managerUsername'] == self.username:
            self.state = 0
        else:
            self.state = 1

        self.surface = pygame.Surface((920, 600))
        self.surface.fill((255, 255, 255))
        self.location = (0, 0)
        self.surface.blit(self.image_left,(0,0))

        self.closeButton = self.createChild(GrayCloseButton, (920 - 50, 15))
        self.minimizeButton = self.createChild(GrayMinimizeButton, (920 - 50 * 2, 15))

        # self.groupAvatar = self.createChild(Image,(75,100),(150,150),'./resources/GroupInforWindowUI/qunliaotouxiang.png')  #####
        self.groupAvatar = self.createChild(GroupInforButton, (75, 100), '', (53, 11), 0, (150, 150),
                                           './resources/GroupInforWindowUI/qunliaotouxiang.png',
                                           './resources/GroupInforWindowUI/qunliaotouxiang.png',
                                           './resources/GroupInforWindowUI/qunliaotouxiang.png')  #####

        #self.avatar = self.createChild(Image, (0, 0), (200, 200), self.tempUser.get("avatarAddress"))
        # self.groupName = self.createChild(text_variable,(90,300),self.groupShow['sessionName'],'simhei',30,(55,55,55))  ######
        n = len(self.groupShow['sessionName'].encode("gbk"))
        self.groupName = self.createChild(text_variable, (int((300-15*n)/2), 300), self.groupShow['sessionName'], 'simhei', 30, (255, 255, 255))
        self.groupNameM = self.createChild(ModifyBar, (0, 300), "群名", self.groupShow['sessionName'], 22)
        self.groupNameM.disable()

        self.quitButton = self.createChild(GroupInforButton,(75,450),'退出群聊',(31,11),22,(150,48),
                                           './resources/GroupInforWindowUI/quit_button_hover.png',
                                           './resources/GroupInforWindowUI/quit_button.png',
                                           './resources/GroupInforWindowUI/quit_button_hover.png')  #####
        self.userListButton = self.createChild(GroupInforButton,(300,56),'成员',(41,2),30,(140,44),
                                               './resources/GroupInforWindowUI/userlist_button.png',
                                               './resources/GroupInforWindowUI/userlist_button.png',
                                               './resources/GroupInforWindowUI/userlist_button.png',)
        self.line = self.createChild(GroupInforButton, (35+300, 100), 'line',(0,0),0,(550,1),
                                               './resources/GroupInforWindowUI/line.png',
                                               './resources/GroupInforWindowUI/line.png',
                                               './resources/GroupInforWindowUI/line.png',)
        self.inviteBg = self.createChild(GroupInforButton, (455 + 300, 56), '允许群成员邀请', (25, 13), 15, (130, 44),
                                     './resources/GroupInforWindowUI/invite_bg.png',
                                     './resources/GroupInforWindowUI/invite_bg.png',
                                     './resources/GroupInforWindowUI/invite_bg.png', )
        self.inviteButton = self.createChild(GroupInforButton, (455 + 300, 70), '', (0, 0), 0, (15, 15),
                                         './resources/GroupInforWindowUI/invite_button.png',
                                         './resources/GroupInforWindowUI/invite_button_select.png',
                                         './resources/GroupInforWindowUI/invite_button_select.png', )
        self.title = self.createChild(GroupInforButton, (19 + 300, 105), '   群成员         群主            操作', (0, 10), 18, (582, 38),
                                             './resources/GroupInforWindowUI/title.png',
                                             './resources/GroupInforWindowUI/title.png',
                                             './resources/GroupInforWindowUI/title.png', )
        self.groupUserList = self.createChild(GroupMemberList, (300, 143), self.groupShow)

        # 功能按钮
        self.editButton = self.createChild(TripleStateButton, (180, 220), './resources/UserInforWinUI/edit.png', (40, 40))
        self.modifyButton = self.createChild(TextButton, (180, 220), "保存", 16, (60, 40))
        self.modifyButton.disable()

        # 添加警示框
        self.showAlert = False
        self.quitAlert = self.createChild(Alert, (285,180), "此举将确定退出群聊，如确认进行操作请再次退出。注：群主退出群聊将解散")

        if self.state != 0:
            self.editButton.disable()
            self.inviteBg.disable()
            self.inviteButton.disable()
        
        
        for tempName in self.groupShow['sessionMembers']:
            request = {
                'messageNumber': '21',
                'keyword': tempName,
            }
            # self.process.requestQueue.put(request)
        print(data['usernameResult']['list'])


    def editInfor(self):
        self.groupName.disable()
        self.groupNameM.enable()
        self.modifyButton.enable()

    def saveInfor(self):
        # 修改用户信息
        self.groupNameM.disable()
        self.modifyButton.disable()
            
        self.groupName.setText(self.groupNameM.inputBox.get_text())
        self.groupName.enable()
            

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        # 当在展示警告框的时候，只让警告框捕获事件
        if self.showAlert:
            for child in self.childs:
                # 如果警告框都是diable，则会自动调整展示状态为False
                self.showAlert = False
                if isinstance(child, Alert) and child.active:
                    self.showAlert = True
                    child.getEvent(event)
        else:
            for child in self.childs:
                if child.active:
                    child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

        # 退出群聊
        if self.quitButton.state == 2 and self.quitButton.isClick == False:
            self.quitButton.isClick = True
            self.quitButton.setState(0)
            self.counter += 1
            if self.counter == 1:
                self.quitAlert.enable()
                self.showAlert = True
            else:
                self.counter = 0
                request = {
                    'messageNumber': '17',
                    'sessionId': self.groupShow['sessionId'],
                }
                self.process.requestQueue.put(request)

        
        # 准备修改信息
        if self.editButton.state == 2:
            self.editButton.setState(0)
            self.editInfor()
        # 保存修改信息
        if self.modifyButton.state == 2:
            self.modifyButton.setState(0)
            request = {
                'messageNumber':'19',
                'sessionId':self.groupShow['sessionId'],
                'sessionName':self.groupNameM.inputBox.get_text(),
            }
            print(request)
            # self.process.requestQueue.put(request)
            self.saveInfor()

    def update(self):
        # # 这里群聊需要判断是不是群主，类似设定状态即可
        # # 判断是否是自己
        # if self.state == 0:
        #     self.addButton.disable()
        #     self.deleteButton.disable()
        # else:
        #     # 判断是否是好友
        #     if self.state == 1:
        #         self.editButton.disable()
        #         self.addButton.disable()
        #     else:
        #         self.editButton.disable()
        #         self.deleteButton.disable()
        for child in self.childs:
            if child.active:
                child.update()
