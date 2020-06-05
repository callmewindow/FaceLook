from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Avatar import Avatar
from FrontEnd.Elements.CustomText import CustomText
from Common.base import readData
import pygame


class SelfInfo(Element):
    image = pygame.image.load('./resources/UserWindowUI/user_info.png')

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (350, 100)
        self.avatar = None
        self.nicknameText = None
        self.surface = SelfInfo.image
        self.refresh()

    def refresh(self):
        self.childs.clear()
        data = readData(self.process.data)
        try:
            self.avatar = self.createChild(Avatar, (15, 15), data['user']['avatarURL'])
            self.nicknameText = self.createChild(CustomText, (100, 36), 'dengxian', 25, (0, 0, 0), data['user']['nickname'])
        except KeyError:
            print('key error in SelfInfo')
