import pygame
from queue import Queue
pygame.init()
class WindowProcess():
    def __init__(self,data,RQ,MQ,bet,window):        
        self.window = window
        self.FPS = 60 
        self.go = True    
        self.data = data
        self.actionList = []
        self.requestQueue = RQ
        self.messageQueue = MQ
        self.bet = bet
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
