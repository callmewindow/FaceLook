import pygame
from FrontEnd.Elements.LoginWindow import LoginWindow
from multiprocessing import Process
from queue import Queue
pygame.init()

class LoginWindowProcess():
    def __init__(self,data):        
        self.window = LoginWindow(self)
        self.FPS = 60 
        self.go = True    
        self.data = data
        self.actionList = []
    def run(self):
        while self.go:
            for event in pygame.event.get():
                if (event.type==pygame.constants.QUIT):
                    pygame.quit() 
                    self.go = False 
                    return 
                self.window.getEvent(event)
            try:
                message = self.messageQueue.get(block=False)
                self.window.getMessage(message)
            except:
                pass
            for action in self.actionList:
                self.getAction(action)
            self.actionList.clear()   
            self.window.display()
            pygame.display.update()
            self.window.FPSClock.tick(self.FPS)
    def addAction(self,action):
        self.actionList.append(action)
    def doAction(self,action):
        pass
    def createSession(self):
        pass
    def getUsernameAndPasswordAndLogin(self):
        #friendList ----- self.data
        pass
def main(data):
    lwp = LoginWindowProcess(data)
    lwp.run()
    return data
