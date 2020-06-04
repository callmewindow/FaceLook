import pygame
from FrontEnd.Elements.SessionWindow import SessionWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from Common.base import *
class SessionWindowProcess():
    def __init__(self,sessionID,data):        
        pygame.init()
        self.FPS = 60 
        self.go = True    
        self.data = data
        self.sessionID = sessionID
        # 先完成窗口内容
        # self.session = self.data.getSessionByID(sessionID)
        # print(self.data)
        # for msg in self.session.userMessages:
        #     print(msg.sender,msg.time,msg.content)
        self.actionList = []
        self.window = SessionWindow(self)
        self.title_rect = (0,0,670,100)
        self.dragging = False
        self.window_pos = (0,0)
        self.mouse_pos = (0,0)
        self.hwnd = self.window.hwnd
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
    def addAction(self,action):
        self.actionList.append(action)
    def doAction(self,action):
        pass
    def stop(self):
        self.go = False
def createSession(sessionID,data):
    swp = SessionWindowProcess(sessionID,data)
    swp.run()