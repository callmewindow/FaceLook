import pygame
from FrontEnd.Elements.UserWindow import UserWindow
from BackEnd.BackEndThread import BackEndThread
from BackEnd.BackEndStaticMethods import *
from multiprocessing import Process
from threading import Thread
from queue import Queue
pygame.init()

    
class UserWindowProcess():
    def __init__(self,data):        
        self.window = UserWindow(self)
        self.data = data
        self.FPS = 60 
        self.go = True        
        self.sessions = []
        self.messageQueue = Queue()
        self.actionList = []
        self.bet = BackEndThread(self.messageQueue,self.data)        
    def run(self):
        self.bet.start()
        while self.go:
            for event in pygame.event.get():
                if (event.type==pygame.constants.QUIT):
                    pygame.quit() 
                    self.bet.stop()
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
        #switch action:
        #self.stop
        pass
    def createSessionWindowProcess(self,SessionID):
        pass
    def stop(self):
        self.go = False
def main(data):
    print(data.login)
    uwp = UserWindowProcess(data)
    uwp.run()

