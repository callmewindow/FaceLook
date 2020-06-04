import pygame
from FrontEnd.Processes.WindowProcess import WindowProcess
from FrontEnd.UnitTest.UnitTestWindow import UnitTestWindow
from Common.base import *
from queue import Queue
class UnitTestProcess(WindowProcess):
    def __init__(self,data,RQ,MQ,bet):  
        WindowProcess.__init__(self,data,RQ,MQ,bet,UnitTestWindow(self))
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
    def doAction(self,action):
        pass

        
        