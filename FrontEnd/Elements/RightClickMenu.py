from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.text_default import text_default
import pygame


class RightClickMenuBlock(Element):
    # block_type==0 发送消息
    # block_type==1 删除
    # block_type==2 修改备注
    image = pygame.Surface((200, 40))
    image.fill((250, 250, 250))
    image_onHover = pygame.Surface((200, 40))
    image_onHover.fill((240, 240, 240))

    def __init__(self, process, location, block_type):
        Element.__init__(self, process)
        self.text = 'test'
        if block_type == 0:
            self.text = '发送消息'
        if block_type == 1:
            self.text = '删除'
        if block_type == 2:
            self.text = '修改备注'
        self.block_text = self.createChild(text_default, (20, 5), self.text, (0, 0, 0))
        self.surface = RightClickMenuBlock.image
        self.location = location
        self.size = (200, 40)
        self.block_type = block_type
        self.user = None

    def pos_in(self, pos):
        x, y = pos[0], pos[1]
        if self.location[0] < x < self.location[0] + self.size[0] and self.location[1] < y < self.location[1] + \
                self.size[1]:
            return True
        return False

    def getEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.pos_in(event.pos):
                self.state = 1
                self.surface = RightClickMenuBlock.image_onHover
            else:
                self.state = 0
                self.surface = RightClickMenuBlock.image
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.pos_in(event.pos):
                print(self.text)
                # do something

    def set_user(self, user):
        self.user = user


class RightClickMenu(Element):
    def __init__(self, process):
        Element.__init__(self, process)
        self.disable()
        self.location = (0, 0)
        self.blocks = []
        for i in range(3):
            self.blocks.append(self.createChild(RightClickMenuBlock, (0, i * 40), i))
        self.surface = pygame.Surface((200, 120))
        self.size = (200, 120)

    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            surface.blit(child.display(), child.location)
        return surface

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.pos_in(event.pos):
                self.disable()
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def pos_in(self, pos):
        x, y = pos[0], pos[1]
        if self.location[0] < x < self.location[0] + self.size[0] and self.location[1] < y < self.location[1] + \
                self.size[1]:
            return True
        return False

    def change_location(self, location):
        self.location = location

    def set_user(self, user):
        for block in self.blocks:
            block.set_user(user)
