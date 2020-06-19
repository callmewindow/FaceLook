from Common.base import *
from FrontEnd.Elements.LoginWindow import LoginWindow
from FrontEnd.Processes.WindowProcessWithoutQueue import WindowProcessWithoutQueue
class LoginWindowProcess(WindowProcessWithoutQueue):
    def __init__(self,data,RQ,MQ,bet):  
        WindowProcessWithoutQueue.__init__(self,data,RQ,MQ,bet,LoginWindow(self))
        self.title_rect = (0,0,650,100)
    def doAction(self,action):
        if action.type == ActionType.LOGIN:
            bg = self.window.bg
            username = bg.usernameInputbox.text
            password = bg.passwordInputbox.text
            data = readData(self.data)
            data['user']['username']=username
            data['user']['password']=password
            data['user']['state'] = UserStateType.OFFLINE
            writeData(self.data,data)
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

        
        