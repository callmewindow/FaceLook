import pygame
from FrontEnd.Elements.UserWindow import UserWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from FrontEnd.Processes.SessionWindowProcess import SessionWindowProcess
from FrontEnd.Processes.SessionWindowProcess import createSession
import multiprocessing
class UserWindowProcess(WindowProcess):
    def __init__(self,data,RQ,MQ,bet): 
        WindowProcess.__init__(self,data,RQ,MQ,bet,UserWindow(self))
        self.window.bg.init()
        self.sessions = []
    def createSessionWindow(self,sessionID):
        proc = multiprocessing.Process(target=createSession,args=(sessionID,))
        proc.start()
