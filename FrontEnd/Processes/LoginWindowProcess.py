import pygame
from FrontEnd.Elements.LoginWindow import LoginWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from Common.base import *
from queue import Queue
class LoginWindowProcess(WindowProcess):
    def __init__(self,data,RQ,MQ,bet):  
        WindowProcess.__init__(self,data,RQ,MQ,bet,LoginWindow(self))
    def doAction(self,action):
        if action.type == ActionType.LOGIN:
            bg = self.window.bg
            username = bg.usernameInputbox.text
            password = bg.passwordInputbox.text
            self.login(username,password)
            self.window.bg.set_loading()
            return
    def login(self,username,password):
        content = 'username: {},password: {}'.format(username,password)
        self.requestQueue.put(Request(RequestType.LOGIN,content))
        