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
from FrontEnd.Elements.Alert import Alert
from BackEnd.LocalStorage import LocalStorage
from Common.base import *

class SessionWindowBackground(Element):
    # type==1 好友私聊
    # type==2 群聊

    def __init__(self,process):
        Element.__init__(self,process)
        data = readData(self.process.data)
        friends = data["friendList"] # 临时使用
        self.username = data['user']['username']
        print('用户名', self.username)
        self.sessionID = self.process.sessionID

        # self.localStorage = LocalStorage('zyx')
        # print(self.localStorage.get_session_content('11'))
        # print(self.localStorage.get_groups())

        print(self.process.localStorage.get_session_content('11'))

        # 从后端获取完整session
        # self.sessionCon
        # self.sessionCon = {
        #     'num_of_message': 3, 
        #     'sessionName': 'zyxandzyx3', 
        #     'managerUsername': 'zyx', 
        #     'sessionMembers': ['zyx', 'zyx3'], 
        #     'last_time': '2020-06-17-22-22-42', 
        #     'last_message': {'kind': '0', 'from': 'zyx', 'time': '2020-06-17-22-22-42', 'to': 'null', 'content': '最后一个测试消息'}, 
        #     'contents': [
        #         {'kind': '0', 'from': 'zyx', 'time': '2020-06-17-22-22-04', 'to': 'null', 'content': '阿萨德'}, 
        #         {'kind': '0', 'from': 'zyx', 'time': '2020-06-17-22-22-32', 'to': 'null', 'content': '张宇轩nb'}, 
        #         {'kind': '0', 'from': 'zyx', 'time': '2020-06-17-22-22-42', 'to': 'null', 'content': '最后一个测试消息'}
        #     ]
        # }
        self.sessionCon = {
            'num_of_message': 3, 
            'sessionName': '', 
            'managerUsername': 'zyx', 
            'sessionMembers': ['zyx', 'zmx'], 
            'last_time': '2020-06-17-22-22-42', 
            'last_message': {'kind': '0', 'from': 'zyx', 'time': '2020-06-17-22-22-42', 'to': 'null', 'content': '最后一个测试消息'}, 
            'contents': [
                {'kind': '0', 'from': 'zyx', 'time': '2020-06-17-22-22-04', 'to': 'null', 'content': '阿萨德'}, 
                {'kind': '0', 'from': 'zyx', 'time': '2020-06-17-22-22-32', 'to': 'null', 'content': '张宇轩nb'}, 
                {'kind': '0', 'from': 'zyx', 'time': '2020-06-17-22-22-42', 'to': 'null', 'content': '最后一个测试消息'}
            ]
        }
        # 如果是好友则在这里直接获取好友信息
        if self.sessionCon['sessionName'] == '':
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
        self.messageList = self.createChild(MessageList,(25,120))

        # 渲染输入框
        self.InputArea = self.createChild(InputArea, (25, marginTop2+50), (850,100), 'simhei', 20, (0,0,0) ,(255,255,255) )
        
        # 空消息警示框
        self.showAlert = False
        self.blankAlert = self.createChild(Alert, (275,250), "不能发送空消息")


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
            # self.process.minimize()
            self.smallButton.setState(0)
            self.process.dragging=False
            self.process.minimize()

        # 关闭
        if self.closeButton.state == 2:
            self.closeButton.setState(0)
            self.process.localStorage = None
            # if self.localStorage != None:
            #     self.localStorage.close()
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
                    'sessionId':'11',
                    'content':{
                        'from':self.username,
                        'to':None,
                        'time':None,
                        'content':self.InputArea.getContent(),
                        'kind':'0',
                    }
                }
                print(request)
                # self.process.requestQueue.put(request)
                # 输入框置空
                self.InputArea.text = ''
                self.InputArea.text_group = ['']
                print(self.localStorage.get_session_content('11'))

    def update(self):
        for child in self.childs:
            if child.active:
                child.update()
        
        
        
        
