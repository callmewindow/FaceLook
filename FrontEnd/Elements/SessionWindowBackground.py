import pygame
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.TripleStateButton import TripleStateButton
from FrontEnd.Elements.IconChangeButton import IconChangeButton
from FrontEnd.Elements.SwitchListBarSession import SwitchListBarSession
from FrontEnd.Elements.TextAreaVariable import TextAreaVariable
from FrontEnd.Elements.TextButton import TextButton
from FrontEnd.Elements.text_variable import text_variable
from FrontEnd.Elements.InputArea import InputArea
from FrontEnd.Elements.MessageList import MessageList
from FrontEnd.Elements.InviteGroupMember import InviteGroupMember
from FrontEnd.Elements.Alert import Alert
from Common.dataFunction import *

class SessionWindowBackground(Element):
    # type==1 好友私聊
    # type==2 群聊

    def __init__(self,process):
        Element.__init__(self,process)
        data = readData(self.process.data)
        self.username = data['user']['username']
        self.sessionId = self.process.sessionId
        friends = data["friendList"]['list'] # 临时使用
        self.sessionCon = {}
        self.sessionVer = -1
        allSession = data['sessionList']['list']
        # 获取完整session
        for session in allSession:
            if session['sessionId'] == self.sessionId:
                self.sessionCon = session
                break

        # 如果是好友则在这里直接获取好友信息
        if self.sessionCon['sessionName'] == None:
            self.type = 1
            if self.sessionCon['sessionMembers'][0] == self.username:
                tempUsername = self.sessionCon['sessionMembers'][1]
            else:
                tempUsername = self.sessionCon['sessionMembers'][0]
            for friend in friends:
                if tempUsername == friend["username"]:
                    self.sessionFriend = friend
            self.title = self.sessionFriend['nickname']
        else:
            self.type = 2
            self.title = self.sessionCon['sessionName']
        
        self.location = (0,0)
        self.surface = pygame.Surface((900,750))
        self.surface.fill((255,255,255))

        # 渲染整体框架
        line = pygame.Surface((900,2))
        line.fill((224, 224, 224))
        # self.surface.blit(line,(0,0))
        titleLeft = (900-12*len(self.title.encode("gbk")))/2
        self.sessionTitle = self.createChild(text_variable, (int(titleLeft),18), self.title, 'simhei', 24, (66, 66, 66))
        marginTop1 = 60
        self.surface.blit(line,(0,marginTop1-2))
        self.surface.blit(line,(0,marginTop1+50))
        marginTop2 = 530
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
        self.addButton = self.createChild(TripleStateButton, (770, marginTop1+8), './resources/SessionWinUI/icons/round_add.png', (34, 34))
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

        # 渲染消息列表，消息的更新在messageList进行
        self.messageList = self.createChild(MessageList,(25,120),self.sessionCon['contents'])

        # 渲染输入框
        self.InputArea = self.createChild(InputArea, (25, marginTop2+50), (850,100), 'simhei', 20, (0,0,0) ,(255,255,255) )
        
        # 空消息警示框
        self.showAlert = False
        self.blankAlert = self.createChild(Alert, (275,250), "不能发送空消息")
        self.imageAlert = self.createChild(Alert, (275,250), "请将图片拖拽到输入框以完成图片的发送")
        self.inviteAlert = self.createChild(Alert, (275,250), "当前群聊不允许群成员邀请好友入群")

        # 群成员邀请框
        self.inviteMember = self.createChild(InviteGroupMember, (600, marginTop1+40), friends)
        self.inviteMember.disable()

        if self.type == 1:
            self.addButton.disable()


    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        # 当在展示警告框的时候，只让警告框捕获事件
        if self.showAlert:
            for child in self.childs:
                # 如果警告框都是diable，则会自动调整展示状态为False
                self.showAlert = False
                if isinstance(child, Alert) and child.active:
                    self.showAlert = True
                    child.getEvent(event)
        else:
            for child in self.childs:
                if child.active:
                    child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

        # 最小化
        if self.smallButton.state == 2:
            self.smallButton.setState(0)
            self.process.dragging=False
            self.process.minimize()

        # 关闭
        if self.closeButton.state == 2:
            self.closeButton.setState(0)
            self.process.stop()
            self.process.dragging=False
        
        # 打开设置窗口
        if self.settingButton.state == 2:
            self.settingButton.setState(0)
            if self.type == 1:
                # 直接传递之前在friends里搜索到的用户信息
                self.process.createUserInforWindow(self.sessionFriend)
            elif self.type == 2:
                # 群聊的信息，直接传递即可
                self.process.createGroupInforWindow(self.sessionCon)
            else:
                pass
        
        # 打开邀请群成员的的窗口
        if self.addButton.state == 2:
            self.addButton.setState(0)
            # 判断是否允许群成员邀请（偷懒判断），不是群主也是官方群则不能邀请
            if self.username != self.sessionCon['managerUsername'] and '官方' in self.sessionCon['sessionName']:
                self.inviteAlert.enable()
                self.showAlert = True
            else:
                self.inviteMember.enable()
        
        # 打开图片发送提示
        if self.pictureButton.state == 2:
            self.pictureButton.setState(0)
            self.imageAlert.enable()
            self.showAlert = True

        # 发送消息
        if self.sendButton.state == 2:
            self.sendButton.setState(1)
            # self.messageList.changeTest()
            if self.InputArea.getContent() == '' or self.InputArea.getContent() == None:
                # 提醒
                self.blankAlert.enable()
                self.showAlert = True
            else:
                request = {
                    'messageNumber':'9',
                    'sessionId':self.sessionId,
                    'content':{
                        'from':self.username,
                        'to':None,
                        'time':None,
                        'content':self.InputArea.getContent(),
                        'kind':'0',
                    }
                }
                self.process.requestQueue.put(request)
                # 输入框置空
                self.InputArea.text = ''
                self.InputArea.text_group = ['']

    def update(self):
        for child in self.childs:
            if child.active:
                child.update()
        
        self.counter = (self.counter+1)%60
        if self.counter < 59: return
        else:
            data = readData(self.process.data)
            # 定时更新session信息
            if data['sessionList']['version'] > self.sessionVer:
                self.sessionVer = data['sessionList']['version']
                allSession = data['sessionList']['list']
                # 获取完整session
                for session in allSession:
                    if session['sessionId'] == self.sessionId:
                        self.sessionCon = session
                        break
                # 是群聊才更新群名称
                if self.type == 2:
                    self.sessionTitle.setText(self.sessionCon['sessionName'])
                self.messageList.getMessages(1,self.sessionCon['contents'])
        
        
        
        
        
