from FrontEnd.Elements.Element import Element
import pygame
from FrontEnd.Elements.PicButton import PicButton


class PicButtonList(Element):

    # state==0 idle
    # state==1 hover
    # state==2 select

    image = pygame.Surface((300, 50))
    image.fill((255,255,255))
    # image = pygame.transform.smoothscale(pygame.image.load('./resources/SessionWinUI/bg/transparent_bg.png'), (340, 50))


    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.size = (300, 50)
        self.buttonSize = (150, 50)

        self.icon1 = self.createChild(PicButton, (0, 0), '', '', self.buttonSize, "申请结果", (35,20))
        self.icon2 = self.createChild(PicButton, (150, 0), '', '', self.buttonSize, "未处理申请",(25,20))
        # self.icon3 = self.createChild(PicButton, (2*85, 0), './resources/SessionWinUI/icons/phone.png', './resources/SessionWinUI/icons/phone_wh.png', self.buttonSize)
        # self.icon4 = self.createChild(PicButton, (3*85, 0), './resources/SessionWinUI/icons/video.png', './resources/SessionWinUI/icons/video_wh.png', self.buttonSize)
        self.icon = [self.icon1, self.icon2]

        self.surface = PicButtonList.image
        self.buttonState = [2, 0]
        self.icon[0].setState(self.buttonState[0])
        self.buttonLocation = [0, 150]
        self.change_from = 0
        self.change_to = 0

        self.changed = False

    def pos_in(self, pos, index):
        x = pos[0]
        y = pos[1]
        if self.buttonLocation[index] < x < self.buttonLocation[index] + self.buttonSize[0] and 0 < y < self.buttonSize[1]:
            return True
        return False


    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        if event.type == pygame.MOUSEMOTION:
            for i in range(2):
                if self.buttonState[i] != 2:
                    if self.pos_in(event.pos, i):
                        self.buttonState[i] = 1
                    else:
                        self.buttonState[i] = 0
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            # if self.pos_in(event.pos,0):
            #     if(self.buttonState[0] != 2):
            #         self.buttonState = [0,0]
            #         self.buttonState[0] = 2
            #         self.change_to = 0
            #         self.changed = True
            # if self.pos_in(event.pos,1):
            #     if(self.buttonState[1] != 2):
            #         self.buttonState = [0, 0]
            #         self.buttonState[1] = 2
            #         self.change_to = 1
            #         self.changed = True
            for i in range(2):
                if self.pos_in(event.pos, i):
                    if self.buttonState[i] != 2:
                        self.buttonState = [0, 0]
                        self.buttonState[i] = 2
                        self.change_to = i
                        self.changed = True
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])


    def display(self):
        surface = self.surface.copy()
        for i in range(2):
            self.icon[i].setState(self.buttonState[i])
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        return surface


###########################################


# class PicListBar(Element):
#     # state==0 idle
#     # state==1 hover
#     # state==2 select
#     image1 = pygame.image.load('./resources/UserWindowUI/switch_0.png')
#     image2 = pygame.image.load('./resources/UserWindowUI/switch_1.png')
#     #icon0 = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/people.png'), (30, 30))
#     icon1 = pygame.Surface((150, 100))
#     icon1.fill((251, 114, 153))
#     icon2 = pygame.Surface((150, 100))
#     icon2.fill((251, 114, 153))
#     #icon1 = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/group.png'), (30, 30))
#     icon1_h = pygame.transform.smoothscale(pygame.image.load('./resources/FriendApplyWindowUI/top_nav_buttonp.png'),
#                                            (150, 100))
#     icon2_h = pygame.transform.smoothscale(pygame.image.load('./resources/FriendApplyWindowUI/top_nav_buttonp.png'),
#                                            (150, 100))
#     icon1_s = pygame.transform.smoothscale(
#         pygame.image.load('./resources/FriendApplyWindowUI/top_nav_buttonp1.png'), (150, 100))
#     icon2_s = pygame.transform.smoothscale(
#         pygame.image.load('./resources/FriendApplyWindowUI/top_nav_buttonp1.png'), (150, 100))
#
#
#     def __init__(self, process, location):
#         Element.__init__(self, process)
#         self.location = location
#         self.size = (300, 50)
#         self.buttonSize = (150, 50)
#         self.icon = [PicListBar.icon1, PicListBar.icon2]
#         self.icon_hover = [PicListBar.icon1_h, PicListBar.icon2_h]
#         self.icon_select = [PicListBar.icon1_s, PicListBar.icon2_s]
#         self.image = [PicListBar.image1, PicListBar.image2]
#         self.buttonState = [2, 0]
#         self.buttonLocation = [0, 150]
#         self.changed = False
#         self.surface = PicListBar.image1
#
#     def pos_in(self, pos):
#         x = pos[0]
#         y = pos[1]
#         if self.location[1] < y < self.size[1] + self.location[1]:
#             if 0 < x < self.size[0] // 2:
#                 return 0
#             elif self.size[0] // 2 < x < self.size[0]:
#                 return 1
#         return -1
#
#     def getEvent(self, event):
#         if event.type == pygame.MOUSEMOTION:
#             target = self.pos_in(event.pos)
#             if target == -1:
#                 if self.buttonState[0] != 2:
#                     self.buttonState[0] = 0
#                 if self.buttonState[1] != 2:
#                     self.buttonState[1] = 0
#             if target != -1 and self.buttonState[target] != 2:
#                 self.buttonState[target] = 1
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
#             target = self.pos_in(event.pos)
#             if target != -1 and self.buttonState[target] != 2:
#                 self.buttonState[target] = 2
#                 self.surface = self.image[target]
#                 self.buttonState[1 - target] = 0
#                 self.changed = True
#
#     def display(self):
#         surface = self.surface.copy()
#         for i in range(2):
#             if self.buttonState[i] == 0:
#                 surface.blit(self.icon[i], (self.buttonLocation[i] + 72, 7))
#             elif self.buttonState[i] == 1:
#                 surface.blit(self.icon_hover[i], (self.buttonLocation[i] + 72, 7))
#             else:
#                 surface.blit(self.icon_select[i], (self.buttonLocation[i] + 72, 7))
#         return surface