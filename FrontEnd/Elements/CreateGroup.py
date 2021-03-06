from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.SingleInputBox import InputBox
from FrontEnd.Elements.TextButton import TextButton
from FrontEnd.Elements.CustomText import CustomText
import pygame


class CreateGroup(Element):
    image = pygame.image.load('./resources/UserWindowUI/create_group.png')

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.disable()
        self.location = location
        self.size = (300, 150)
        self.surface = CreateGroup.image
        self.createChild(CustomText, (20, 20), 'simhei', 16, (0, 0, 0), '请输入群名')
        self.input = self.createChild(InputBox, (20, 60), 260, 'simhei', 20, (0, 0, 0), (245, 245, 245))
        self.send = self.createChild(SendButton, (220, 105), '创建', 16, (60, 25))

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and not self.pos_in(event.pos):
            self.input.text = ''
            self.input.update()
            self.disable()
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            if child.active:
                child.getEvent(event)
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] <= x <= self.location[0] + self.size[0] \
                and self.location[1] <= y <= self.location[1] + self.size[1]:
            return True
        return False

    def update(self):
        if self.send.pressed:
            self.process.requestQueue.put({
                'messageNumber': '6',
                'sessionName': self.input.text,
            })
            self.process.requestQueue.put({'messageNumber': '5'})
            self.input.text = ''
            self.input.update()
            self.disable()
        self.send.pressed = False
        for child in self.childs:
            if child.active:
                child.update()


class SendButton(TextButton):

    def __init__(self, process, location, text, fontsize, size):
        TextButton.__init__(self, process, location, text, fontsize, size)
        self.pressed = False

    def getEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.state != 2:
                if self.pos_in(event.pos):
                    self.state = 1
                else:
                    self.state = 0
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and self.pos_in(event.pos):
                self.state = 2
            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                self.state = 0
                if self.pos_in(event.pos):
                    self.pressed = True
