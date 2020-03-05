import pygame
from FrontEnd.Elements.UserWindow import UserWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from BackEnd.BackEndThread import BackEndThread
from BackEnd.BackEndStaticMethods import *
class UserWindowProcess(WindowProcess):
    def __init__(self,data,RQ,MQ,bet): 
        WindowProcess.__init__(self,data,RQ,MQ,bet,UserWindow(self))       


