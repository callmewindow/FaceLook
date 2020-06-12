import pygame
from FrontEnd.Elements.UserInforWindow import UserInforWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from FrontEnd.Processes.AlertWindowProcess import createAlert
import multiprocessing
from Common.base import *
from queue import Queue
import pyautogui
import win32gui

class UserInforWindowProcess(WindowProcess):
    def __init__(self,userShow,data,RQ,MQ):
        bet = None
        self.data = data
        # temp = {'username': 'MinatoAqu', 'nickname': 'kotori', 'invitee': 1, 'avatarAddress': 'cd37c244-6558-42de-8fd4-770f75d1be8e', 'phoneNumber': '114514', 'email': '1919810', 'occupation': 'senpai', 'location': 'Japan'}
        self.userShow = userShow # 传一个完整的user对象即可
        WindowProcess.__init__(self,data,RQ,MQ,bet,UserInforWindow(self))
        # 只有这里需要调用init函数，历史遗留内容
        self.window.bg.init()
    
    def createAlertWindow(self, content):
        proc = multiprocessing.Process(target=createAlert,
                                       args=(content, self.data, self.requestQueue, self.messageQueue))
        proc.start()

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

def createUserInfor(userShow,data,RQ,MQ):
    uiwp = UserInforWindowProcess(userShow,data,RQ,MQ)
    uiwp.run()