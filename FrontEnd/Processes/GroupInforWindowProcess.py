import pygame
from FrontEnd.Elements.GroupInforWindow import GroupInforWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
import multiprocessing
from Common.base import *
from queue import Queue
import pyautogui
import win32gui

class GroupInforWindowProcess(WindowProcess):
    # 这里不一定可以直接传一个group对象（因为是session），所以可能需要传入id后再从data中找出来
    def __init__(self,groupShow,data,RQ,MQ):
        bet = None
        self.data = data
        temp = 	{'sessionId': 11, 'numOfMessage': 0, 'sessionName': 'zyxandzyx3', 'managerUsername': 'zyx', 'sessionMembers': ['zyx', 'zyx3'], 'contents': [{'kind': '0', 'from': 'zyx', 'time': '2020-06-17-22-22-04', 'to': 'null', 'content': '阿萨德'}, {'kind': '0', 'from': 'zyx', 'time': '2020-06-17-22-22-32', 'to': 'null', 'content': '张宇轩nb'}, {'kind': '0', 'from': 'zyx', 'time': '2020-06-17-22-22-42', 'to': 'null', 'content': '最后一个测试消息'}, {'kind': '0', 'from': 'zyx', 'time': '2020-06-18-23-26-30', 'to': 'null', 'content': '阿萨德'}, {'kind': '0', 'from': 'zyx', 'time': '2020-06-18-23-26-51', 'to': 'null', 'content': '再次测试'}]},
        self.groupShow = temp # 传一个完整的user对象即可
        WindowProcess.__init__(self,data,RQ,MQ,bet,GroupInforWindow(self))
        # 只有这里需要调用init函数，历史遗留内容
        self.window.bg.init()

    def run(self):
        while self.go:
            if self.dragging:
                new_mouse_pos = pyautogui.position()
                if new_mouse_pos[0]!=self.mouse_pos[0] or new_mouse_pos[1]!=self.mouse_pos[1]:
                    new_window_pos = (self.window_pos[0]+new_mouse_pos[0]-self.mouse_pos[0],
                                      self.window_pos[1]+new_mouse_pos[1]-self.mouse_pos[1])
                    self.window.set_location(new_window_pos)
            for event in pygame.event.get():
                if (event.type==pygame.constants.QUIT):
                    pygame.display.quit()
                    self.go = False 
                    return 
                if (event.type==pygame.MOUSEBUTTONDOWN and event.button==pygame.BUTTON_LEFT and self.dragging==False and
                    event.pos[0]>=self.title_rect[0] and event.pos[0]<=self.title_rect[2] and
                    event.pos[1]>=self.title_rect[1] and event.pos[1]<=self.title_rect[3]):
                    self.dragging = True
                    windowRect = win32gui.GetWindowRect(self.hwnd)
                    self.window_pos = (windowRect[0],windowRect[1])
                    self.mouse_pos = pyautogui.position()
                    del windowRect
                if (event.type==pygame.MOUSEBUTTONUP and event.button==pygame.BUTTON_LEFT and self.dragging==True):
                    self.dragging = False
                self.window.getEvent(event)
            for action in self.actionList:
                self.doAction(action)
            self.actionList.clear()   
            self.window.display()
            pygame.display.update()
            self.window.FPSClock.tick(self.FPS)

def createGroupInfor(groupShow,data,RQ,MQ):
    uiwp = GroupInforWindowProcess(groupShow,data,RQ,MQ)
    uiwp.run()