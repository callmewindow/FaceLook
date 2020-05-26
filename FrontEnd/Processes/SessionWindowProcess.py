import pygame
from FrontEnd.Elements.SessionWindow import SessionWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from Common.base import *
from queue import Empty
class SessionWindowProcess():
    def __init__(self,sessionID):        
        pygame.init()
        self.FPS = 60 
        self.go = True    
        self.RQ = RQ
        self.MQ = MQ
        self.sessionID = sessionID
        self.actionList = []
        self.window = SessionWindow(self)
    def run(self):
        while self.go:
            for event in pygame.event.get():
                if (event.type==pygame.constants.QUIT):
                    pygame.display.quit()
                    self.go = False 
                    return 
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
def createSession(sessionID):
    swp = SessionWindowProcess(sessionID)
    swp.run()