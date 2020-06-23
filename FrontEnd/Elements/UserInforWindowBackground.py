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
from FrontEnd.Elements.AddCheckMessage import AddCheckMessage
from FrontEnd.Elements.Alert import Alert
from Common.dataFunction import *

class UserInforWindowBackground(Element):
    # state == 0 本人
    # state == 1 好友
    # state == 2 陌生人

    topbg = pygame.Surface((500, 200))
    topbg.fill((251, 114, 153))
    
    def __init__(self, process):
        Element.__init__(self, process)
        self.surface = pygame.Surface((500, 600))
        self.surface.fill((255, 255, 255))
        self.location = (0, 0)
        # 获取自己的用户名和展示的用户
        self.state = -1
        self.tempUser = self.process.userShow
        data = readData(self.process.data)
        friends = data["friendList"]['list']
        self.username = data["user"]["username"]
        if self.tempUser.get("username") == self.username:
            self.state = 0
        else:
            self.state = 2 # 先默认认为是陌生人
            for friend in friends:
                if self.tempUser.get("username") == friend["username"]:
                    self.state = 1 # 有重复的则是好友

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
        self.checkMessage = self.createChild(AddCheckMessage, (0, 220))
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

        # 添加警示框
        self.showAlert = False
        self.deleteAlert = self.createChild(Alert, (75,200), "此举将会删除双方的好友关系，如果确认请再次点击删除按钮")

        # 判断是否是自己
        if self.state == 0:
            self.addButton.disable()
            self.deleteButton.disable()
        else:
            # 判断是否是好友
            if self.state == 1:
                self.editButton.disable()
                self.addButton.disable()
            else:
                self.editButton.disable()
                self.deleteButton.disable()
        
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
        
        # 添加好友
        if self.addButton.state == 2:
            self.addButton.setState(0)
            self.checkMessage.set_username(self.username)
            self.checkMessage.enable()

        # 删除好友
        if self.deleteButton.state == 2:
            self.deleteButton.setState(0)
            self.counter += 1
            if self.counter == 1:
                self.deleteAlert.enable()
                self.showAlert = True
            else:
                self.counter = 0
                request = {
                    'messageNumber':'15',
                    'username':self.tempUser.get('username'),
                }
                self.process.requestQueue.put(request)
                # 然后窗口关闭
                self.process.stop()
                self.process.dragging = False

        # 准备修改信息
        if self.editButton.state == 2:
            self.editButton.setState(0)
            self.editInfor()
        # 不修改信息
        if self.returnButton.state == 2:
            self.returnButton.setState(0)
            self.returnInit(False)
        # 保存修改信息
        if self.modifyButton.state == 2:
            self.modifyButton.setState(0)
            if self.inviteeM.inputBox.get_text() == "允许":
                tempInvite = 1
            else:
                tempInvite = 0
            request = {
                'messageNumber':'18',
                'nickname': self.nickname2M.inputBox.get_text(),
                'avatarAddress': self.avatar.url,
                'invitee': tempInvite,
                'phoneNumber': self.phonenumM.inputBox.get_text(),
                'email': self.mailM.inputBox.get_text(),
                'occupation': self.majorM.inputBox.get_text(),
                'location':self.addressM.inputBox.get_text()
            }
            self.process.requestQueue.put(request)
            self.returnInit(True)

    def update(self):
        for child in self.childs:
            if child.active:
                child.update()
