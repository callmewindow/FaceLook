import pygame
from FrontEnd.Elements.LoginWindow import LoginWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from Common.base import *
from queue import Queue
class LoginWindowProcess(WindowProcess):
    def __init__(self,data,RQ,MQ,bet):  
        WindowProcess.__init__(self,data,RQ,MQ,bet,LoginWindow(self))
        self.title_rect = (0,0,650,100)
    def doAction(self,action):
        if action.type == ActionType.LOGIN:
            bg = self.window.bg
            username = bg.usernameInputbox.text
            password = bg.passwordInputbox.text
            self.data['user']['username']=username
            self.data['user']['password']=password
            self.data['user']['state'] = UserStateType.OFFLINE
            self.login(username,password)
            self.window.bg.set_loading()
            return
    def login(self,username,password):
        request = {            
            'messageNumber':'2',
            'messageField1':username,
            'messageField2':password,
            }
        self.requestQueue.put(request)

        
        