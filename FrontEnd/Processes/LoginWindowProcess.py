import pygame
from FrontEnd.Elements.LoginWindow import LoginWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from BackEnd.BackEndThread import BackEndThread
from BackEnd.BackEndStaticMethods import *
class LoginWindowProcess(WindowProcess):
    def __init__(self,data):  
        WindowProcess.__init__(self,data,LoginWindow(self))      
        self.bet = BackEndThread(self.requestQueue,self.messageQueue)   
        print(self.window.surface.get_rect())
def main(data):
    lwp = LoginWindowProcess(data)
    lwp.run()
    return data 
