import pygame
from FrontEnd.Elements.SessionWindow import SessionWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from Common.base import *
class SessionWindowProcess(WindowProcess):
    def __init__(self,sessionID,data,RQ,MQ):     
        bet = None
        self.data = data
        self.sessionID = sessionID
        WindowProcess.__init__(self, data, RQ, MQ, bet, SessionWindow(self))
        print(self.data)

    def doAction(self,action):
        if action.type == "send":
            bg = self.window.bg
            inputCon = bg.getInputCon()
            print(inputCon) # 还是会输出多次
            self.sendMessage(inputCon)
            return
    
    def sendMessage(self,inputCon):
        # request = {
        #     'messageNumber':'x',
        #     'messageField1':username,
        #     'messageField2':password,
        #     }
        # self.requestQueue.put(request)
        pass
    
    # def createSessionWindow(self, sessionID):
    #     # proc = multiprocessing.Process(target=createSession,
    #     #                                args=(sessionID, self.data, self.requestQueue, self.messageQueue))
    #     # proc.start()
    #     print("生成会话")
    #     pass

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

def createSession(sessionID,data,RQ,MQ):
    swp = SessionWindowProcess(sessionID,data,RQ,MQ)
    swp.run()