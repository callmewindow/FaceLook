import pygame
from FrontEnd.Elements.UserWindow import UserWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from BackEnd.BackEndThread import BackEndThread
from BackEnd.BackEndStaticMethods import *
class UserWindowProcess(WindowProcess):
    def __init__(self,data): 
        WindowProcess.__init__(self,data,UserWindow(self))       
        self.bet = BackEndThread(self.messageQueue,self.data)

def main(data):
    print(data.login)
    uwp = UserWindowProcess(data)
    uwp.run()
    return data

