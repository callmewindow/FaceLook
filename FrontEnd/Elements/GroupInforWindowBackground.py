import pygame
from Common.base import *
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.SelfInfo import SelfInfo
from FrontEnd.Elements.text_variable import text_variable
from FrontEnd.Elements.InforBar import InforBar
from FrontEnd.Elements.TripleStateButton import TripleStateButton

class GroupInforWindowBackground(Element):
    topbg = pygame.Surface((400, 150))
    topbg.fill((240, 240, 240))
    
    friend = dict(
            uid='wyx84',
            remark='至尊',
            nickname='灭天魔王', 
            phonenum='18201314307', 
            address='火星',
            mail='847590417@qq.com',
            major='英雄',
            friend='true'
            )
    stranger = dict(
        uid='wyx84',
        nickname='灭天魔王', 
        phonenum='18201314307', 
        address='火星',
        mail='847590417@qq.com',
        major='英雄',
        friend='false'
        )
    me = dict(
        uid='wyx8475',
        nickname='灭天魔王', 
        phonenum='18201314307', 
        address='火星',
        mail='847590417@qq.com',
        major='英雄',
        )
    def __init__(self, process):
        Element.__init__(self, process)
        self.surface = pygame.Surface((400, 500))
        self.surface.fill((255, 255, 255))
        self.location = (0, 0)
        # 获取数据
        self.uid='wyx8475'
        self.tempUser = self.friend

    def init(self):
        # 绘制上半部分内容
        self.surface.blit(self.topbg, (0, 0))
        self.avatar = pygame.transform.smoothscale(pygame.image.load('./resources/UserData/MinatoAqua/MinatoAqua.jpg'), (150, 150))
        self.surface.blit(self.avatar, (0, 0))
        self.nickname1 = self.createChild(text_variable, (175, 25),self.tempUser.get("nickname"), 'simhei', 25, (0,0,0))
        self.editButton = self.createChild(TripleStateButton, (270, 135), './resources/UserInforWinUI/edit.png', (30, 30))

        # 添加具体信息
        topY = 210
        self.username = self.createChild(InforBar, (100, topY), "用户名", self.tempUser.get("uid"), 16)
        self.nickname2 = self.createChild(InforBar, (100, topY+30), "昵称", self.tempUser.get("nickname"), 16)
        self.phonenum = self.createChild(InforBar, (100, topY+60), "手机号", self.tempUser.get("phonenum"), 16)
        self.mail = self.createChild(InforBar, (100, topY+90), "邮箱", self.tempUser.get("mail"), 16)
        self.major = self.createChild(InforBar, (100, topY+120), "职业", self.tempUser.get("major"), 16)
        self.address = self.createChild(InforBar, (100, topY+150), "所在地", self.tempUser.get("address"), 16)
        
        # 添加功能按钮
        self.addButton = self.createChild(TripleStateButton, (10, 460), './resources/UserInforWinUI/add.png', (60, 30))
        self.deleteButton = self.createChild(TripleStateButton, (330, 460), './resources/UserInforWinUI/delete.png', (60, 30))

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    # def getState(self):
    #     return self.button.state

    def testChange(self):
        self.tempUser = dict(uid='wyx847590417', nickname='车干', phonenum='123456', address='山东菏泽')

    def update(self):
        # 判断是否是自己
        if self.tempUser.get("uid") == self.uid:
            self.addButton.disable()
            self.deleteButton.disable()
        else:
            # 判断是否是好友
            if self.tempUser.get("friend") == "true":
                self.addButton.disable()
            else:
                self.editButton.disable()
                self.deleteButton.disable()

        for child in self.childs:
            if child.active:
                child.update()
