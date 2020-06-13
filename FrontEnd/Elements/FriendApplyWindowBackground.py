from FrontEnd.Elements.FriendApplyList import ReceiverList, RequestorList
from FrontEnd.Elements.text_variable import text_variable
from FrontEnd.Elements.InputArea import InputArea
from FrontEnd.Elements.MessageList import MessageList
from Common.base import *
from FrontEnd.Elements.TopNavBar import TopNavBar
from FrontEnd.Elements.BottomNavBar import BottomNavBar
from FrontEnd.Elements.PicButtonList import PicButtonList
from FrontEnd.Elements.Button import *
from FrontEnd.Elements.FriendList import FriendList
# from FrontEnd.Elements.FriendApplyList import *

class FriendApplyWindowBackground(Element):
    flag = False

    def __init__(self,process):

        self.flag = False

        Element.__init__(self,process)

        surfaceWidth = 750
        surfaceHeight = 800
        self.surface = pygame.Surface((surfaceWidth, surfaceHeight))
        self.surface.fill((255, 255, 255))
        self.location = (0, 0)

        # 顶部导航栏
        self.top_nav_bar = self.createChild(TopNavBar, (0, 0))
        self.title_text = self.createChild(text_variable, (30, 15), "好友验证", 'simhei', 18, (244, 248, 244))
        # 窗口切换按钮列表
        self.pic_button_list = self.createChild(PicButtonList, (0, 50))

        # 验证消息列表
        self.receiver_list = self.createChild(ReceiverList, (0, 110))  # 多向下10px
        self.requestor_list = self.createChild(RequestorList, (750,110))

        # 底部导航栏
        self.bottom_nav_bar = self.createChild(BottomNavBar, (0, 750))

        #窗口控制按钮
        self.closeButton = self.createChild(CloseButton, (750 - 50, 15))
        self.minimizeButton = self.createChild(MinimizeButton, (750 - 50 * 2, 15))

        self.displayed_list = 0

    def getEvent(self, event):
        for child in self.childs:
            if child.active:
                child.getEvent(event)

    def update(self):
        movespeed = 750   #需要是windowwidth = 750 的因数
        margintop = 110   #和列表初始化时距离顶端的位置一样

        if self.pic_button_list.changed:
            self.receiver_list.enable()
            self.requestor_list.enable()
            if self.displayed_list == 0 and self.requestor_list.location[0] > 0:
                self.receiver_list.location = (self.receiver_list.location[0] - movespeed, margintop)
                self.requestor_list.location = (self.requestor_list.location[0] - movespeed, margintop)
            elif self.displayed_list == 1 and self.receiver_list.location[0] < 0:
                self.receiver_list.location = (self.receiver_list.location[0] + movespeed, margintop)
                self.requestor_list.location = (self.requestor_list.location[0] + movespeed, margintop)
            else:
                self.pic_button_list.changed = False
                self.displayed_list = 1 - self.displayed_list
                if self.displayed_list == 0:
                    self.requestor_list.disable()
                else:
                    self.receiver_list.disable()

        for child in self.childs:
            if child.active:
                child.update()
