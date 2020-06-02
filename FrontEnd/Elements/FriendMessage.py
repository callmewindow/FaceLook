from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.text_variable import text_variable
from FrontEnd.Elements.TextAreaVariable import TextAreaVariable
import pygame

class FriendMessage(Element):
    pygame.font.init()

    bg = pygame.Surface((620, 0))

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
        self.sender = self.createChild(text_variable,(0,5),sender.get("name"),'simhei',14,nameColor)
        timeLeft = 7*len(sender.get("name").encode("gbk"))
        self.time = self.createChild(text_variable,(timeLeft+10,6),time,'simhei',12,(120,120,120))

        # 消息内容
        self.content = self.createChild(TextAreaVariable,(0,24),620,0,'./resources/SessionWinUI/bg/transparent_bg.png','simhei',16,content,(0,0,0))
        self.bg = pygame.Surface((620,30+self.content.surface.get_size()[1]))
        self.bg.fill((255,255,255))
        self.surface = self.bg

