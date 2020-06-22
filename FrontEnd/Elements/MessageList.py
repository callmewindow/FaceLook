import pygame
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.FriendMessage import FriendMessage
from FrontEnd.Elements.MessageRightClick import MessageRightClick

class MessageList(Element):
    # 针对获取message的类型
    # type==0 初始化
    # type==1 更新消息列表

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

        self.getMessages(0,contents)

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

    def getMessages(self,type,contents=None):
        if type == 0:
            # 初始化
            self.sessionContents = contents
            for message in self.sessionContents:
                MessageList.messages.append(self.createChild(FriendMessage, (0,0), message, self.rightClickMenu))
        else:
            # 更新消息列表
            self.sessionContents = contents
            tempLen = len(self.sessionContents)
            if tempLen == MessageList.msgLen:
                # 如果消息列表没更新则返回
                return
            for i in range(MessageList.msgLen, tempLen):
                MessageList.messages.append(self.createChild(FriendMessage, (0,0), self.sessionContents[i], self.rightClickMenu))
                MessageList.messages[i].disable()
            
            # tempLen = len(MessageList.messages)
            # for i in (MessageList.msgLen, tempLen-1):

            # 如果在底部消息将会自动滚动
            if self.toIndex >= MessageList.msgLen-1 and self.topMargin <= 400:
                MessageList.msgLen = tempLen
                self.topMargin = 444
                self.fromIndex = -1
                while self.topMargin > 400:
                    self.drawMessage("down")
            
            # 保证消息长度的更新
            MessageList.msgLen = tempLen

    def update(self):
        for child in self.childs:
            if child.active:
                child.update()
    
    # def addTest(self):
    #     # sender0 = dict(uid="847590417", name="王宇轩")
    #     # MessageList.messages.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/7/1 15:54:09", "text::更新测试1",self.rightClickMenu))
    #     # MessageList.messages.append(self.createChild(FriendMessage, (0, 0), sender0, "2020/7/1 15:54:09", "text::更新测试2",self.rightClickMenu))
        
    #     # 处理新增的消息记录
    #     tempLen = len(MessageList.messages)
    #     for i in (MessageList.msgLen, tempLen-1):
    #         MessageList.messages[i].disable()

    #     # 如果在底部消息将会自动滚动
    #     if self.toIndex >= MessageList.msgLen-1 and self.topMargin <= 400:
    #         MessageList.msgLen = tempLen
    #         self.topMargin = 444
    #         self.fromIndex = -1
    #         while self.topMargin > 400:
    #             self.drawMessage("down")
        
    #     # 保证消息长度的更新
    #     MessageList.msgLen = tempLen

