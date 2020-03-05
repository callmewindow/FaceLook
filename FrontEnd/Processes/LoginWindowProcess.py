import pygame
from FrontEnd.Elements.LoginWindow import LoginWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
class LoginWindowProcess(WindowProcess):
    def __init__(self,data,RQ,MQ,bet):  
        WindowProcess.__init__(self,data,RQ,MQ,bet,LoginWindow(self))      