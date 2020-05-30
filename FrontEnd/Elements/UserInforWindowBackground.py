from Common.base import *
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.SelfInfo import SelfInfo
from FrontEnd.Elements.InforBar import InforBar
from FrontEnd.Elements.TripleStateButton import TripleStateButton
import pygame

class UserInforWindowBackground(Element):
    topbg = pygame.Surface((400, 150))
    topbg.fill((184, 178, 178))

    def __init__(self, process):
        Element.__init__(self, process)
        self.surface = pygame.Surface((400, 600))
        self.surface.fill((255, 255, 255))
        self.location = (0, 0)
        self.tempUser = dict(uid='wyx847590417', nickname='軒', phonenum='18201314307', address='山东菏泽')

    def init(self):
        # 绘制上半部分内容
        self.surface.blit(self.topbg, (0, 0))
        self.avatar = pygame.transform.smoothscale(pygame.image.load('./resources/UserData/MinatoAqua/MinatoAqua.jpg'), (100, 100))
        self.surface.blit(self.avatar, (40, 25))
        self.editButton = self.createChild(TripleStateButton, (160, 100), './resources/UserInforWinUI/edit.png', \
            './resources/UserInforWinUI/edit_hover.png', './resources/UserInforWinUI/edit_select.png', (30, 30))

        # 添加具体信息
        self.nickname1 = self.createChild(InforBar, (105, 250), "", self.tempUser.get("nickname"), 30)
        self.username = self.createChild(InforBar, (100, 300), "用户名", self.tempUser.get("uid"), 16)
        self.nickname2 = self.createChild(InforBar, (100, 330), "昵称", self.tempUser.get("nickname"), 16)
        self.phonenum = self.createChild(InforBar, (100, 360), "手机号", self.tempUser.get("phonenum"), 16)
        self.nickname2 = self.createChild(InforBar, (100, 390), "所在地", self.tempUser.get("address"), 16)

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def get_state(self):
        return self.button.state

    def testChange(self):
        self.tempUser = dict(uid='wyx847590417', nickname='车干', phonenum='123456', address='山东菏泽')


    def update(self):
        for child in self.childs:
            if child.active:
                child.update()
