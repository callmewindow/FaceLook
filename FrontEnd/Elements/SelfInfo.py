from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Avatar import Avatar
from FrontEnd.Elements.CustomText import CustomText
from FrontEnd.Elements.Image import Image
from Common.base import readData
import pygame


class SelfInfo(Element):
    image = pygame.image.load('./resources/UserWindowUI/user_info.png')

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (350, 129)
        self.avatar = None
        self.nicknameText = None
        self.surface = SelfInfo.image
        data = readData(self.process.data)
        try:
            self.avatar = self.createChild(Avatar, (27, 27), data['user']['avatarURL'])
            # self.avatar = self.createChild(Image, (27, 27), data['user']['avatarURL'][7:])
            self.nickname = self.createChild(CustomText, (120, 50), 'dengxian', 26, (0, 0, 0), data['user']['nickname'])
        except KeyError:
            print('key error in SelfInfo')

    def refresh(self):
        self.childs.clear()

