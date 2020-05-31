import pygame
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.TripleStateButton import TripleStateButton
from FrontEnd.Elements.IconChangeButton import IconChangeButton
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
        self.surface = pygame.Surface((670,520))
        self.surface.fill((255,255,255))

        # 渲染整体框架
        line = pygame.Surface((670,1))
        line.fill((224, 224, 224))
        # self.surface.blit(line,(0,0))
        titleLeft = (670-12*len(self.sessionInfor.get("title").encode("gbk")))/2
        self.sessionTitle = self.createChild(text_variable, (int(titleLeft),12), self.sessionInfor.get("title"), 'simhei', 20, (0,0,0))
        marginTop1 = 44
        self.surface.blit(line,(0,marginTop1))
        self.surface.blit(line,(0,marginTop1+36))
        marginTop2 = 380
        self.surface.blit(line,(0,marginTop2))
        self.surface.blit(line,(0,marginTop2+30))

        # 渲染按钮部分
        # 窗口切换按钮
        self.chatButton = self.createChild(IconChangeButton, (0, marginTop1), './resources/SessionWinUI/icons/message.png', './resources/SessionWinUI/icons/message_wh.png', (70, 36))
        self.fileButton = self.createChild(IconChangeButton, (70, marginTop1), './resources/SessionWinUI/icons/file.png', './resources/SessionWinUI/icons/file_wh.png', (70, 36))
        self.phoneButton = self.createChild(IconChangeButton, (140, marginTop1), './resources/SessionWinUI/icons/phone.png', './resources/SessionWinUI/icons/phone_wh.png', (70, 36))
        self.videoButton = self.createChild(IconChangeButton, (210, marginTop1), './resources/SessionWinUI/icons/video.png', './resources/SessionWinUI/icons/video_wh.png', (70, 36))
        
        # 其他功能按钮
        self.settingButton = self.createChild(TripleStateButton, (610, marginTop1+5), './resources/SessionWinUI/icons/setting.png', (28, 28))
        
        self.emojiButton = self.createChild(TripleStateButton, (15, marginTop2+3), './resources/SessionWinUI/icons/emoji.png', (24, 24))
        self.vioceButton = self.createChild(TripleStateButton, (15+60, marginTop2+3), './resources/SessionWinUI/icons/voice.png', (24, 24))
        self.cutButton = self.createChild(TripleStateButton, (15+120, marginTop2+3), './resources/SessionWinUI/icons/cut.png', (24, 24))
        self.pictureButton = self.createChild(TripleStateButton, (15+180, marginTop2+3), './resources/SessionWinUI/icons/picture.png', (24, 24))
        self.uploadButton = self.createChild(TripleStateButton, (15+240, marginTop2+3), './resources/SessionWinUI/icons/upload.png', (24, 24))
        self.historyButton = self.createChild(TripleStateButton, (615, marginTop2+2), './resources/SessionWinUI/icons/history.png', (27, 27))

        self.sendButton = self.createChild(TextButton, (605, 480), "发送", 15, (50, 25))

        # 渲染消息列表
        self.messageList = self.createChild(MessageList,(25,82))

        # 渲染输入框
        self.tempInputBox = self.createChild(TextAreaVariable, (15, marginTop2+35), 490, 0 , 'white', 'simhei', 16, "Facelook第二次迭代准备开始！|", (0, 0, 0))


    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])


    def update(self):
        for child in self.childs:
            if child.active:
                child.update()
    
        
        
        
        
