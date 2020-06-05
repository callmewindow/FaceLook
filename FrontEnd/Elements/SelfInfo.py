from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Avatar import Avatar
from FrontEnd.Elements.CustomText import CustomText
import pygame


class SelfInfo(Element):
    image = pygame.image.load('./resources/UserWindowUI/user_info.png')

    def __init__(self, process, location, user):
        Element.__init__(self, process)
        self.location = location
        self.user = user
        self.size = (350, 100)
        self.avatar = self.createChild(Avatar, (15, 15), user['avatarURL'])
        self.nicknameText = self.createChild(CustomText, (100, 36), 'dengxian', 25, (0, 0, 0), user['nickname'])
        self.surface = SelfInfo.image
