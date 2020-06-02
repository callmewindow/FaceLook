from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.CustomText import CustomText
import pygame


class RightClickMenuBlock(Element):
    # block_type==0 发送消息
    # block_type==1 修改备注
    # block_type==2 查看资料
    # block_type==3 删除
    # block_type==4 申请好友
    image = pygame.transform.smoothscale(pygame.image.load('./resources/UserWindowUI/transparent_background.png'),
                                         (120, 40))
    image_onHover = pygame.Surface((120, 40))
    image_onHover.fill((230, 230, 230))
    image_onHover.set_alpha(200)

    def __init__(self, process, location, block_type):
        Element.__init__(self, process)
        if block_type == 0:
            self.text = '发送消息'
        elif block_type == 1:
            self.text = '修改备注'
        elif block_type == 2:
            self.text = '查看资料'
        elif block_type == 3:
            self.text = '删除'
        elif block_type == 4:
            self.text = '发送申请'
        self.block_text = self.createChild(CustomText, (16, 12), 'simhei', 16, (0, 0, 0), self.text)
        self.surface = RightClickMenuBlock.image
        # self.surface = pygame.font.SysFont('simhei', 16).render(self.text, True, (0, 0, 0))
        self.location = location
        self.size = (120, 40)
        self.block_type = block_type
        self.user = None

    def pos_in(self, pos):
        x, y = pos[0], pos[1]
        if self.location[0] < x < self.location[0] + self.size[0] \
                and self.location[1] < y < self.location[1] + self.size[1]:
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
                if self.text == '发送消息':
                    self.process.createSessionWindow(233)

                # do something

    def set_user(self, user):
        self.user = user
