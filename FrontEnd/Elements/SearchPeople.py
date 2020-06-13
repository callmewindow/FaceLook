from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.TextButton import TextButton
from FrontEnd.Elements.CustomText import CustomText
from FrontEnd.Elements.Image import Image
from Common.base import readData, writeData
import pygame


class PeopleBlock(Element):

    def __init__(self, process, location, user, check):
        Element.__init__(self, process)
        self.surface = pygame.Surface((200, 80))
        self.surface.fill((255, 255, 255))
        self.location = location
        self.size = (200, 80)
        self.check = check
        self.avatar = self.createChild(Image, (15, 15), (50, 50), user['avatarAddress'])
        self.nickname = self.createChild(CustomText, (75, 10), 'simhei', 20, (0, 0, 0), user['nickname'], 190)
        self.add = self.createChild(AddButton, (80, 45), '+好友', 12, (40, 20), user['username'], check)

    def getEvent(self, event):
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            if child.active:
                child.getEvent(event)
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])


class SearchPeople(Element):

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.surface = pygame.Surface((800, 400))
        self.surface.fill((255, 255, 255))
        self.location = location
        self.size = (800, 400)
        self.check = None
        self.counter = 0

    def getEvent(self, event):
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            if child.active:
                child.getEvent(event)
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def update(self):
        self.counter = (self.counter + 1) % 60
        if self.counter == 0:
            data = readData(self.process.data)
            try:
                if 'search_nickname' in data and len(data['search_nickname']) != 0:
                    x, y = 0, 0
                    for user in data['search_nickname']:
                        self.createChild(PeopleBlock, (x, y), user, self.check)
                        x = (x + 200) % 800
                        y += 80 if x == 0 else 0
                    data['search_nickname'].clear()
                    writeData(self.process.data, data)
                elif 'search_username' in data and len(data['search_username']) != 0:
                    x, y = 0, 0
                    for user in data['search_username']:
                        self.createChild(PeopleBlock, (x, y), user, self.check)
                        x = (x + 200) % 800
                        y += 80 if x == 0 else 0
                    data['search_username'].clear()
                    writeData(self.process.data, data)
            except KeyError:
                print('key error in search')
        for child in self.childs:
            if child.active:
                child.update()


class AddButton(TextButton):

    def __init__(self, process, location, text, fontsize, size, username, check):
        TextButton.__init__(self, process, location, text, fontsize, size)
        self.username = username
        self.check = check

    def getEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.pos_in(event.pos):
                if self.state != 2:
                    self.state = 1
            else:
                self.state = 0
            return
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP] and self.pos_in(event.pos):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                self.state = 2
            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                self.state = 0
                if self.pos_in(event.pos):
                    self.check.set_username(self.username)
                    self.check.enable()
