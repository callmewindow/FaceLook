from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.CustomText import CustomText
from FrontEnd.Elements.text_variable import text_variable
import pygame

class GroupInforButton(Element):
    image = pygame.transform.smoothscale(pygame.image.load('./resources/FriendApplyWindowUI/Frame 6.png'), (60, 30))
    image_hover = pygame.transform.smoothscale(pygame.image.load('./resources/FriendApplyWindowUI/Frame 8.png'), (60, 30))
    image_select = pygame.transform.smoothscale(pygame.image.load('./resources/FriendApplyWindowUI/Frame 8.png'), (60, 30))
    def __init__(self, process, location, text, text_location,font_size,button_size,image_url,image_hover_url,image_select_url):
        Element.__init__(self, process)
        self.size = button_size
        self.image = pygame.transform.smoothscale(pygame.image.load(image_url), self.size)
        self.image_hover = pygame.transform.smoothscale(pygame.image.load(image_hover_url), self.size)
        self.image_select = pygame.transform.smoothscale(pygame.image.load(image_select_url), self.size)
        self.location = location
        self.state = 0
        self.font_size = font_size
        self.isClick = False
        #显示文字
        self.text = self.createChild(text_variable, text_location, text, 'simhei', self.font_size, (55, 55, 55))


    # 为了在状态切换中使用，去除了原本的状态改变能力
    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] <= x <= self.location[0] + self.size[0] \
                and self.location[1] <= y <= self.location[1] + self.size[1]:
            return True
        return False

    def getEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.state != 2:
                if self.pos_in(event.pos):
                    self.state = 1
                else:
                    self.state = 0
        # if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and self.isClick == False:
        #     if self.pos_in(event.pos):
        #         if self.state != 2:
        #             self.state = 2
        #             self.isClick = True
        #         else:
        #             self.state = 1
        #     else:
        #         self.state = 0
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and self.isClick == False:
            if self.pos_in(event.pos):
                if self.state != 2:
                    self.state = 2
                    # self.isClick = True
                else:
                    self.state = 1
            else:
                self.state = 0

    def setState(self, stateType):
        self.state = stateType


    def display(self):
        if self.state == 0:
            self.surface = self.image
        elif self.state == 1:
            self.surface = self.image_hover
        else:
            self.surface = self.image_select
        surface = self.surface.copy()
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        return surface