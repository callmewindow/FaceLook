import pygame
from FrontEnd.Elements.UserInforWindow import UserInforWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from FrontEnd.Processes.SessionWindowProcess import SessionWindowProcess
from FrontEnd.Processes.SessionWindowProcess import createSession
import multiprocessing

class UserInforWindowProcess(WindowProcess):
    def __init__(self,data,RQ,MQ,bet):
        WindowProcess.__init__(self,data,RQ,MQ,bet,UserInforWindow(self))
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
    
    # 打开修改信息窗口
    def createModifyWindow(self,userId,data):
        # 判断修改的对象类型
        if userId == self.uid:
            # 修改自身信息
            pass
        else:
            # 修改好友信息
            pass
    
    # 添加好友
    def addFriend(self,friendId):
        print(friendId)

    # 删除好友
    def deleteFriend(self,friendId):
        print(friendId)

    # 向好友发起会话
    def createSessionWindow(self,sessionID):
        proc = multiprocessing.Process(target=createSession,args=(sessionID,self.data))
        proc.start()
