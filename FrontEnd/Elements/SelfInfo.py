from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.CustomText import CustomText
from FrontEnd.Elements.Image import Image
from Common.base import readData
import pygame


class SelfInfo(Element):
    image = pygame.image.load('./resources/UserWindowUI/user_info.png')
    avatar_cover = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/news.png'), (75, 75))

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (350, 129)
        self.avatar = None
        self.nicknameText = None
        self.surface = SelfInfo.image
        self.covered = False
        data = readData(self.process.data)
        try:
            self.user = data['user']
            self.avatar = self.createChild(Image, (27, 27), (75, 75), self.user['avatarAddress'])
            self.nickname = self.createChild(CustomText, (120, 50), 'simhei', 26, (0, 0, 0), self.user['nickname'], 200)
        except KeyError:
            print('key error in SelfInfo')

    def pos_in_avatar(self, pos):
        x = pos[0]
        y = pos[1]
        if 27 < x < 27 + 75 and 27 < y < 27 + 75:
            return True

    def refresh(self):
        data = readData(self.process.data)
        try:
            self.user = data['user']
            self.avatar.change(self.user['avatarAddress'])
            self.nickname.set_text(self.user['nickname'])
        except KeyError:
            print('key error in SelfInfo when refresh')

    def getEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.pos_in_avatar(event.pos):
                self.covered = True
            else:
                self.covered = False
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.pos_in_avatar(event.pos):
                self.process.createInfoWindow(self.user)

    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        if self.covered:
            surface.blit(SelfInfo.avatar_cover, (27, 27))
        return surface
