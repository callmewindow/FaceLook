import pygame
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.FriendMessage import FriendMessage
from FrontEnd.Elements.MessageRightClick import MessageRightClick


class MessageList(Element):
        #aqua = self.createChild(Aqua,(450,300))
        # self.session = self.data.getSessionByID(sessionID)
        # print(self.data)
        # for msg in self.session.userMessages:
        #     print(msg.sender,msg.time,msg.content)
    # msg模拟获取到的process的消息
    msg = []

    messages = []
    fromIndex = 0
    toIndex = 0
    topMargin = 0
    msgLen = 0
    
    def __init__(self, process, location, contents):
        Element.__init__(self,process)
        self.location = location
        self.surface = pygame.Surface((850,400))
        self.surface.fill((255,255,255))
        self.rightClickMenu = self.createChild(MessageRightClick, (850,400))
        # print(contents)
        # sender0 = dict(uid="847590417", name="王宇轩")
        # sender1 = dict(uid="123456", name="张宇轩")
        # sender2 = dict(uid="654321", name="邓诗曼")
        # MessageList.msg.append(self.createChild(FriendMessage, (0, 0), sender1, "2020/6/5 15:10:12", "image::54907ad7-0749-4ef9-91eb-3d00de047446",self.rightClickMenu))
        # MessageList.msg.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/6/5 15:15:30", "image::79c192d9-b27e-40db-9e77-0b324ca8f8ee",self.rightClickMenu))
        # MessageList.msg.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/6/31 15:43:31", "text::好，给100w的facelook币，尽情花费",self.rightClickMenu))
        # MessageList.msg.append(self.createChild(FriendMessage, (0, 0), sender1, "2020/6/31 15:51:10", "text::上上学期华为云是用啥登录来着\n（熊猫摸耳）",self.rightClickMenu))
        # MessageList.msg.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/6/5 15:15:30", "image::79c192d9-b27e-40db-9e77-0b324ca8f8ee",self.rightClickMenu))
        # MessageList.msg.append(self.createChild(FriendMessage, (0, 0), sender2, "2020/6/31 15:54:09", "text::https://devcloud.huaweicloud.com",self.rightClickMenu))
        # MessageList.msg.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/7/1 15:54:09", "text::图片测试0",self.rightClickMenu))
        # MessageList.msg.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/6/5 15:15:30", "image::8cefb1d1-6b66-4433-b04e-d7e2874fd555",self.rightClickMenu))
        for message in contents:
            MessageList.msg.append(self.createChild(FriendMessage, (0,0), message, self.rightClickMenu))

        MessageList.messages = self.msg
        MessageList.msgLen = len(MessageList.messages)
        for i in range(MessageList.msgLen):
            MessageList.messages[i].disable()

        self.topMargin = 444
        self.fromIndex = -1
        while self.topMargin > 400:
            self.drawMessage("down")
        
    def messageReset(self):
        self.topMargin = 0
        i = self.fromIndex
        if i < 0 : return
        while i < self.toIndex:
            MessageList.messages[i].location = (0,0)
            MessageList.messages[i].disable()
            i += 1

    def drawMessage(self, direction): 
        # print(self.fromIndex, self.toIndex)
        if direction == "top":
            # 当第一个消息渲染的时候才是到顶
            if self.fromIndex <= 0:
                # print("到头了")
                return
            self.messageReset()
            self.fromIndex -= 1
            self.toIndex = self.fromIndex
            while self.toIndex < MessageList.msgLen:
                index = self.toIndex
                MessageList.messages[index].location = (0, self.topMargin)
                MessageList.messages[index].enable()
                self.topMargin += MessageList.messages[index].surface.get_size()[1]
                self.toIndex += 1
                if self.topMargin > 400: break
        
        if direction == "down":
            # 只有当最后一个消息完全显示而且是最后一个消息的时候才是到底
            if self.toIndex >= MessageList.msgLen-1 and self.topMargin <= 400:
                # print("到底了")
                return
            self.messageReset()
            self.fromIndex += 1
            self.toIndex = self.fromIndex
            while self.toIndex < MessageList.msgLen:
                index = self.toIndex
                MessageList.messages[index].location = (0, self.topMargin)
                MessageList.messages[index].enable()
                self.topMargin += MessageList.messages[index].surface.get_size()[1]
                self.toIndex += 1
                if self.topMargin > 400: break
    
    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        # 保证右键菜单一直在前
        if self.rightClickMenu.active:
            surface.blit(self.rightClickMenu.display(), self.rightClickMenu.location)
        return surface

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            if child.active:
                child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_WHEELDOWN:
                self.drawMessage("down")
            if event.button == pygame.BUTTON_WHEELUP:
                self.drawMessage("top")
    
    def update(self):
        for child in self.childs:
            if child.active:
                child.update()
        self.counter = (self.counter+1)%60
        if self.counter < 59: return
        # 直接增加即可，如果更新会每次强制到底部，无法记录位置
        # self.addTest()
    
    def addTest(self):
        # sender0 = dict(uid="847590417", name="王宇轩")
        # MessageList.messages.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/7/1 15:54:09", "text::更新测试1",self.rightClickMenu))
        # MessageList.messages.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/7/1 15:54:09", "text::更新测试2",self.rightClickMenu))
        
        # 处理新增的消息记录
        tempLen = len(MessageList.messages)
        for i in (MessageList.msgLen, tempLen-1):
            print(i)
            MessageList.messages[i].disable()

        # 如果在底部消息将会自动滚动
        if self.toIndex >= MessageList.msgLen-1 and self.topMargin <= 400:
            MessageList.msgLen = tempLen
            self.topMargin = 444
            self.fromIndex = -1
            while self.topMargin > 400:
                self.drawMessage("down")
        
        # 保证消息长度的更新
        MessageList.msgLen = tempLen

