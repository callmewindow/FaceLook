from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.text_variable import text_variable
from FrontEnd.Elements.TextAreaVariable import TextAreaVariable
from FrontEnd.Elements.Image import Image
import pygame

class FriendMessage(Element):
    pygame.font.init()

    bg = pygame.Surface((850, 0))

    uid = "847590417"

    def __init__(self, process, location, sender, time, content):
        Element.__init__(self, process)
        self.location = location
        self.surface = None

        # 消息头部
        if sender.get("uid") == self.uid:
            nameColor = (226, 130, 130)
        else:
            nameColor = (124, 177, 252)
        self.sender = self.createChild(text_variable,(0,4),sender.get("name"),'simhei',18,nameColor)
        timeLeft = 9*len(sender.get("name").encode("gbk"))
        self.time = self.createChild(text_variable,(timeLeft+10,6),time,'simhei',15,(120,120,120))

        # 消息内容
        if content.startswith("text::"):
            self.content = self.createChild(TextAreaVariable,(0,26),850,0,'./resources/SessionWinUI/bg/transparent_bg.png','simhei',20,content[6:],(0,0,0))
        elif content.startswith("image::"):
            self.content = self.createChild(Image,(0,26),(50,50),content[7:])
        self.bg = pygame.Surface((900,32+self.content.surface.get_size()[1]))
        self.bg.fill((255,255,255))
        self.surface = self.bg

