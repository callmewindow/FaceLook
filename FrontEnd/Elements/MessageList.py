import pygame
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.FriendMessage import FriendMessage


class MessageList(Element):
        #aqua = self.createChild(Aqua,(450,300))
        # self.session = self.data.getSessionByID(sessionID)
        # print(self.data)
        # for msg in self.session.userMessages:
        #     print(msg.sender,msg.time,msg.content)
    messages = []
    fromIndex = 0
    toIndex = 0
    topMargin = 0
    
    def __init__(self, process, location):
        Element.__init__(self,process)
        self.location = location
        self.surface = pygame.Surface((850,400))
        self.surface.fill((255,255,255))
        sender0 = dict(uid="847590417", name="王宇轩")
        sender1 = dict(uid="123456", name="张宇轩")
        sender2 = dict(uid="654321", name="邓诗曼")
        MessageList.messages.append(self.createChild(FriendMessage, (0, 0), sender1, "2020/6/5 15:10:12", "image::54907ad7-0749-4ef9-91eb-3d00de047446"))
        MessageList.messages.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/6/5 15:15:30", "image::79c192d9-b27e-40db-9e77-0b324ca8f8ee"))
        self.messages.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/6/31 15:43:31", "text::好，给100w的facelook币，尽情花费"))
        self.messages.append(self.createChild(FriendMessage, (0, 0), sender1, "2020/6/31 15:51:10", "text::上上学期华为云是用啥登录来着\n（熊猫摸耳）"))
        MessageList.messages.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/6/5 15:15:30", "image::79c192d9-b27e-40db-9e77-0b324ca8f8ee"))
        self.messages.append(self.createChild(FriendMessage, (0, 0), sender2, "2020/6/31 15:54:09", "text::https://devcloud.huaweicloud.com"))
        self.messages.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/7/1 15:54:09", "text::图片测试"))
        MessageList.messages.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/6/5 15:15:30", "image::8cefb1d1-6b66-4433-b04e-d7e2874fd555"))
        
        for i in range(len(MessageList.messages)):
            self.messages[i].disable()

        self.topMargin = 0
        self.fromIndex = 0
        self.toIndex = self.fromIndex
        while self.toIndex < len(MessageList.messages):
            index = self.toIndex
            self.messages[index].location = (0, self.topMargin)
            self.messages[index].enable()
            self.topMargin += self.messages[index].surface.get_size()[1]
            self.toIndex += 1
            if self.topMargin > 400: break
        
    
    def messageReset(self):
        self.topMargin = 0
        i = self.fromIndex
        while i < self.toIndex:
            self.messages[i].location = (0,0)
            self.messages[i].disable()
            i += 1

    def drawMessage(self, direction): 
        print(self.fromIndex)
        print(self.toIndex)
        if direction == "top":
            # 当第一个消息渲染的时候才是到顶
            if self.fromIndex <= 0:
                print("到头了")
                return
            print("尝试上升")
            self.messageReset()
            self.fromIndex -= 1
            self.toIndex = self.fromIndex
            while self.toIndex < len(MessageList.messages):
                index = self.toIndex
                self.messages[index].location = (0, self.topMargin)
                self.messages[index].enable()
                self.topMargin += self.messages[index].surface.get_size()[1]
                self.toIndex += 1
                if self.topMargin > 400: break

        
        if direction == "down":
            # 只有当最后一个消息完全显示的时候才是到底
            if self.topMargin <= 400:
                print("到底了")
                return
            print("尝试下降")
            self.messageReset()
            self.fromIndex += 1
            self.toIndex = self.fromIndex
            while self.toIndex < len(MessageList.messages):
                index = self.toIndex
                self.messages[index].location = (0, self.topMargin)
                self.messages[index].enable()
                self.topMargin += self.messages[index].surface.get_size()[1]
                self.toIndex += 1
                if self.topMargin > 400: break

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_WHEELDOWN:
                self.drawMessage("down")
            if event.button == pygame.BUTTON_WHEELUP:
                self.drawMessage("top")