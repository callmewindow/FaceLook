import pygame
from FrontEnd.Elements.UserWindow import UserWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
class UserWindowProcess(WindowProcess):
    def __init__(self,data,RQ,MQ,bet): 
        WindowProcess.__init__(self,data,RQ,MQ,bet,UserWindow(self))       
