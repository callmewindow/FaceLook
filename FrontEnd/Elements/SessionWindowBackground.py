import pygame
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.TripleStateButton import TripleStateButton
from FrontEnd.Elements.IconChangeButton import IconChangeButton
from FrontEnd.Elements.SwitchListBarSession import SwitchListBarSession
from FrontEnd.Elements.TextAreaVariable import TextAreaVariable
from FrontEnd.Elements.TextButton import TextButton
from FrontEnd.Elements.text_variable import text_variable
from FrontEnd.Elements.FriendMessage import FriendMessage
from Common.base import Session
class MessageList(Element):
        #aqua = self.createChild(Aqua,(450,300))
        # self.session = self.data.getSessionByID(sessionID)
        # print(self.data)
        # for msg in self.session.userMessages:
        #     print(msg.sender,msg.time,msg.content)
    
    def __init__(self, process, location):
        Element.__init__(self,process)
        self.location = location
        self.surface = pygame.Surface((620,295))
        self.surface.fill((255,255,255))
        sender0 = dict(uid="847590417", name="王宇轩")
        sender1 = dict(uid="123456", name="张宇轩")
        sender2 = dict(uid="654321", name="邓诗曼")
        self.messages = []
        self.messages.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/5/31 15:43:31", "好，给1w的facelook币，尽情花费"))
        self.messages.append(self.createChild(FriendMessage, (0, 0), sender1, "2020/5/31 15:51:10", "上学期华为云是用啥登录来着\n（熊猫摸耳）"))
        self.messages.append(self.createChild(FriendMessage, (0, 0), sender2, "2020/5/31 15:54:09", "https://devcloud.huaweicloud.com\n切到北京1"))
        self.messages.append(self.createChild(FriendMessage, (0, 0), sender1, "2020/5/31 15:54:38", "thx"))
        messageMargin = 10
        for i in range(len(self.messages)):
            self.messages[i].location = (0, messageMargin)
            messageMargin += self.messages[i].surface.get_size()[1]
        
        
class SessionWindowBackground(Element):

    sessionInfor=dict(title="Facelook开发团队")

    def __init__(self,process):
        Element.__init__(self,process)
        self.location = (0,0)
        self.surface = pygame.Surface((900,750))
        self.surface.fill((255,255,255))

        # 渲染整体框架
        line = pygame.Surface((900,2))
        line.fill((224, 224, 224))
        # self.surface.blit(line,(0,0))
        titleLeft = (900-12*len(self.sessionInfor.get("title").encode("gbk")))/2
        self.sessionTitle = self.createChild(text_variable, (int(titleLeft),19), self.sessionInfor.get("title"), 'simhei', 22, (0,0,0))
        marginTop1 = 60
        self.surface.blit(line,(0,marginTop1-2))
        self.surface.blit(line,(0,marginTop1+50))
        marginTop2 = 520
        self.surface.blit(line,(0,marginTop2))
        self.surface.blit(line,(0,marginTop2+40))

        # 渲染按钮部分
        # 窗口切换按钮
        self.switchList = self.createChild(SwitchListBarSession, (0, marginTop1))

        # 窗口控制按钮
        controlBtnSize = (28,28)
        self.smallButton = self.createChild(TripleStateButton, (770, 14), './resources/WindowControlUI/move.png', controlBtnSize)
        self.bigButton = self.createChild(TripleStateButton, (770+45, 14), './resources/WindowControlUI/square.png', controlBtnSize)
        self.closeButton = self.createChild(TripleStateButton, (770+90, 14), './resources/WindowControlUI/close.png', controlBtnSize)
        
        # 其他功能按钮
        self.settingButton = self.createChild(TripleStateButton, (830, marginTop1+8), './resources/SessionWinUI/icons/setting.png', (34, 34))
        
        leftMargin = 30
        functionBtnSize = (30,30)
        self.emojiButton = self.createChild(TripleStateButton, (leftMargin, marginTop2+5), './resources/SessionWinUI/icons/emoji.png', functionBtnSize)
        self.vioceButton = self.createChild(TripleStateButton, (leftMargin+60, marginTop2+5), './resources/SessionWinUI/icons/voice.png', functionBtnSize)
        self.cutButton = self.createChild(TripleStateButton, (leftMargin+120, marginTop2+5), './resources/SessionWinUI/icons/cut.png', functionBtnSize)
        self.pictureButton = self.createChild(TripleStateButton, (leftMargin+180, marginTop2+5), './resources/SessionWinUI/icons/picture.png', functionBtnSize)
        self.uploadButton = self.createChild(TripleStateButton, (leftMargin+240, marginTop2+5), './resources/SessionWinUI/icons/upload.png', functionBtnSize)
        self.historyButton = self.createChild(TripleStateButton, (840, marginTop2+4), './resources/SessionWinUI/icons/history.png', (32, 32))

        self.sendButton = self.createChild(TextButton, (810, 690), "发送", 18, (65, 35))

        # # 渲染消息列表
        # self.messageList = self.createChild(MessageList,(25,82))

        # # 渲染输入框
        # self.tempInputBox = self.createChild(TextAreaVariable, (leftMargin, marginTop2+35), 490, 0 , 'white', 'simhei', 16, "Facelook第二次迭代准备开始！|", (0, 0, 0))


    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

        # 最小化
        if self.smallButton.state == 2:
            self.process.minimize()
            self.smallButton.setState(0)

        # 关闭
        if self.closeButton.state == 2:
            self.process.close()
            self.closeButton.setState(0)

    def update(self):
        for child in self.childs:
            if child.active:
                child.update()
    
        
        
        
        
