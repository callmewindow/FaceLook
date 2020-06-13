from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Avatar import Avatar
from FrontEnd.Elements.CustomText import CustomText
from Common.base import readData
from FrontEnd.Elements.TripleStateButton import TripleStateButton
from FrontEnd.Elements.PicButton import PicButton
from FrontEnd.Elements.SwitchListBarSession import SwitchListBarSession
import pygame


class TopNavBar(Element):
    image = pygame.image.load('./resources/FriendApplyWindowUI/top_nav_bar.png')

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (750, 100)
        self.surface = TopNavBar.image

        # 切换按钮
        # marginTop1 = 60
        # self.switchList = self.createChild(SwitchListBarSession, (0, marginTop1))

    #   self.refresh()

    # def getEvent(self, event):
    #     if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
    #         event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
    #     for child in self.childs:
    #         child.getEvent(event)
    #     if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
    #         event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])


    # def refresh(self):
    #     self.childs.clear()
    #     data = readData(self.process.data)
    #     try:
    #         self.avatar = self.createChild(Avatar, (15, 15), data['user']['avatarURL'])
    #         self.nicknameText = self.createChild(CustomText, (100, 36), 'dengxian', 25, (0, 0, 0), data['user']['nickname'])
    #     except KeyError:
    #         print('key error in SelfInfo')
