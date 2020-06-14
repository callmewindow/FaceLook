from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.text_variable import text_variable
from FrontEnd.Elements.TextAreaVariable import TextAreaVariable
from FrontEnd.Elements.Image import Image
from Common.base import readData
import pygame

class FriendMessage(Element):
    # state==0 idle
    # state==1 hover
    # state==2 select

    # type==0 message 和好友块统一

    # kind==0 文本
    # kind==1 图片
    # kind==2 文件
    pygame.font.init()
    bg = pygame.Surface((850, 0))

    def __init__(self, process, location, content, menu):
        Element.__init__(self, process)
        data = readData(self.process.data)
        self.username = data["user"]["username"]

        self.location = location
        self.surface = None
        self.senderName = content["from"]
        self.time = content["time"]
        self.content = content["content"]
        self.kind = content["kind"]
        # 消息头部
        if self.senderName == self.username:
            nameColor = (226, 130, 130)
        else:
            nameColor = (124, 177, 252)
        self.sender = self.createChild(text_variable,(0,4),self.senderName,'simhei',18,nameColor)
        timeLeft = 9*len(self.senderName.encode("gbk"))
        self.time = self.createChild(text_variable,(timeLeft+10,6),self.formatTime(self.time),'simhei',15,(120,120,120))

        # 消息内容
        if self.kind == '0':
            self.message = self.createChild(TextAreaVariable,(0,26),850,0,'./resources/SessionWinUI/bg/transparent_bg.png','simhei',20,self.content,(0,0,0))
        elif self.kind == '1':
            self.message = self.createChild(Image,(0,26),(50,50),self.content)
        else:
            pass
        self.bg = pygame.Surface((900,32+self.message.surface.get_size()[1]))
        self.bg.fill((255,255,255))
        self.surface = self.bg
        self.size = (self.surface.get_size()[0],self.surface.get_size()[1])

        # 右键菜单及附加内容
        self.type = 0
        self.state = 0
        self.rightClickMenu = menu
    
    def formatTime(self, time):
        return time[0:4]+'/'+time[5:7]+'/'+time[8:10]+' '+time[11:13]+':'+time[14:16]+':'+time[17:19]

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] < x < self.location[0] + self.size[0] \
                and self.location[1] < y < self.location[1] + self.size[1]:
            return True
        return False

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT and self.pos_in(event.pos):
            self.rightClickMenu.change_location(event.pos)
            # 从sender中获取user后才能set
            # self.rightClickMenu.set_user(self.user)
            self.rightClickMenu.enable()

    def is_displayed(self):
        if -350 < self.location[0] < 350 and 0 <= self.location[1] <= 400:
            return True
        return False
