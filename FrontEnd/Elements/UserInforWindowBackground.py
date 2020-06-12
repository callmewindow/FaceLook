import pygame
from Common.base import *
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.SelfInfo import SelfInfo
from FrontEnd.Elements.text_variable import text_variable
from FrontEnd.Elements.InforBar import InforBar
from FrontEnd.Elements.ModifyBar import ModifyBar
from FrontEnd.Elements.TripleStateButton import TripleStateButton
from FrontEnd.Elements.TextButton import TextButton
from FrontEnd.Elements.Image import Image
from FrontEnd.Elements.Button import UserCloseButton
from FrontEnd.Elements.SingleInputBox import InputBox
from Common.base import readData

class UserInforWindowBackground(Element):
    topbg = pygame.Surface((500, 200))
    topbg.fill((251, 114, 153))
    
    temp = {'username': 'zyx', 'nickname': 'kotori', 'invitee': 1, 'avatarAddress': 'cd37c244-6558-42de-8fd4-770f75d1be8e', 'phoneNumber': '114514', 'email': '1919810', 'occupation': 'senpai', 'location': 'Japan'}
    def __init__(self, process):
        Element.__init__(self, process)
        self.surface = pygame.Surface((500, 600))
        self.surface.fill((255, 255, 255))
        self.location = (0, 0)
        # 获取自己的用户名和展示的用户
        data = readData(self.process.data)
        self.username = data['user']['username']
        self.tempUser = self.temp

    def init(self):
        # 绘制上半部分内容
        self.surface.blit(self.topbg, (0, 0))
        self.avatar = self.createChild(Image, (0, 0), (200, 200), self.tempUser.get("avatarAddress"))
        self.nickname1 = self.createChild(text_variable, (235, 40),self.tempUser.get("nickname"), 'simhei', 30, (0,0,0))
        self.editButton = self.createChild(TripleStateButton, (420, 185), './resources/UserInforWinUI/edit.png', (40, 40))
        self.closeButton = self.createChild(UserCloseButton, (450, 15))

        # 添加具体信息
        topY = 230
        self.username = self.createChild(InforBar, (150, topY), "用户名", self.tempUser.get("username"), 20)
        self.nickname2 = self.createChild(InforBar, (150, topY+40), "昵称", self.tempUser.get("nickname"), 20)
        self.phonenum = self.createChild(InforBar, (150, topY+80), "手机号", self.tempUser.get("phoneNumber"), 20)
        self.mail = self.createChild(InforBar, (150, topY+120), "邮箱", self.tempUser.get("email"), 20)
        self.major = self.createChild(InforBar, (150, topY+160), "职业", self.tempUser.get("occupation"), 20)
        self.address = self.createChild(InforBar, (150, topY+200), "所在地", self.tempUser.get("location"), 20)
        getInvite = self.tempUser.get("invitee")
        if getInvite == 1:
            self.inviteeT = "允许"
        else:
            self.inviteeT = "不允许"
        self.invitee = self.createChild(InforBar, (150, topY+240), "邀请入群", self.inviteeT, 20)
        
        # 添加功能按钮
        self.addButton = self.createChild(TripleStateButton, (10, 540), './resources/UserInforWinUI/add.png', (80, 40))
        self.deleteButton = self.createChild(TripleStateButton, (410, 540), './resources/UserInforWinUI/delete.png', (80, 40))

        # 添加修改信息的内容
        self.nickname2M = self.createChild(ModifyBar, (150, topY+40), "昵称", self.tempUser.get("nickname"), 20)
        self.phonenumM = self.createChild(ModifyBar, (150, topY+80), "手机号", self.tempUser.get("phoneNumber"), 20)
        self.mailM = self.createChild(ModifyBar, (150, topY+120), "邮箱", self.tempUser.get("email"), 20)
        self.majorM = self.createChild(ModifyBar, (150, topY+160), "职业", self.tempUser.get("occupation"), 20)
        self.addressM = self.createChild(ModifyBar, (150, topY+200), "所在地", self.tempUser.get("location"), 20)
        self.inviteeM = self.createChild(ModifyBar, (150, topY+240), "邀请入群", self.inviteeT, 20)
        self.modifyButton = self.createChild(TextButton, (410, 540), "保存", 18, (80, 40))
        self.returnButton = self.createChild(TripleStateButton, (10, 540), './resources/UserInforWinUI/delete.png', (80, 40))
        self.returnInit(False)

    def editInfor(self):
        self.nickname1.disable()
        self.nickname2.disable()
        self.phonenum.disable()
        self.mail.disable()
        self.major.disable()
        self.address.disable()
        self.invitee.disable()
        self.editButton.disable()
        self.addButton.disable()
        self.deleteButton.disable()
        
        self.nickname2M.enable()
        self.phonenumM.enable()
        self.mailM.enable()
        self.majorM.enable()
        self.addressM.enable()
        self.inviteeM.enable()
        self.modifyButton.enable()
        self.returnButton.enable()

    def returnInit(self, modify):
        if not modify:
            self.nickname2M.disable()
            self.phonenumM.disable()
            self.mailM.disable()
            self.majorM.disable()
            self.addressM.disable()
            self.inviteeM.disable()
            self.modifyButton.disable()
            self.returnButton.disable()

            self.nickname1.enable()
            self.nickname2.enable()
            self.phonenum.enable()
            self.mail.enable()
            self.major.enable()
            self.address.enable()
            self.invitee.enable()
            self.editButton.enable()
            self.addButton.enable()
            self.deleteButton.enable()
        else: # 修改用户信息
            self.nickname2M.disable()
            self.phonenumM.disable()
            self.mailM.disable()
            self.majorM.disable()
            self.addressM.disable()
            self.inviteeM.disable()
            self.modifyButton.disable()
            self.returnButton.disable()

            self.nickname1.setText(self.nickname2M.inputBox.get_text())
            self.nickname1.enable()
            self.nickname2.setContent(self.nickname2M.inputBox.get_text())
            self.phonenum.setContent(self.phonenumM.inputBox.get_text())
            self.mail.setContent(self.mailM.inputBox.get_text())
            self.major.setContent(self.majorM.inputBox.get_text())
            self.address.setContent(self.addressM.inputBox.get_text())
            self.invitee.setContent(self.inviteeM.inputBox.get_text())
            self.editButton.enable()
            self.addButton.enable()
            self.deleteButton.enable()

            if self.inviteeM.inputBox.get_text() == "允许":
                tempInvite = 1
            else:
                tempInvite = 0
            temp = {
                'nickname': self.nickname2M.inputBox.get_text(),
                'invitee': tempInvite,
                'phoneNumber': self.phonenumM.inputBox.get_text(),
                'email': self.mailM.inputBox.get_text(),
                'occupation': self.majorM.inputBox.get_text(),
                'location':self.addressM.inputBox.get_text()
            }
            self.process.doAction(Action("modify",temp))

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            if child.active:
                child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])
        
        # 修改信息
        if self.editButton.state == 2:
            self.editButton.setState(0)
            self.editInfor()
        # 不修改信息
        if self.returnButton.state == 2:
            self.returnButton.setState(0)
            self.returnInit(False)
        # 保存修改信息
        if self.modifyButton.state == 2:
            print(123)
            self.modifyButton.setState(0)
            self.returnInit(True)
        

    def getEditState(self):
        return self.editButton.state

    def update(self):
        # 判断是否是自己
        if self.tempUser.get("username") == self.username:
            self.addButton.disable()
            self.deleteButton.disable()
        else:
            # 判断是否是好友
            # if self.tempUser.get("friend") == "true":
            #     self.addButton.disable()
            # else:
            #     self.editButton.disable()
            #     self.deleteButton.disable()
            pass
        
        for child in self.childs:
            if child.active:
                child.update()
