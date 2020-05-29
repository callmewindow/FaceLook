import pygame
from FrontEnd.Elements.UserInforWindow import UserInforWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
class UserInforWindowProcess(WindowProcess):
    def __init__(self,data,RQ,MQ,bet): 
        WindowProcess.__init__(self,data,RQ,MQ,bet,UserInforWindow(self))
        self.window.bg.init()
    
    def modifyUserInfor(self,newUserData):
        print(newUserData)
