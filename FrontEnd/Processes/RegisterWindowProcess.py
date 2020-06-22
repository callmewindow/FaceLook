from Common.base import *
from FrontEnd.Elements.RegisterWindow import RegisterWindow
from FrontEnd.Processes.WindowProcessWithoutQueue import WindowProcessWithoutQueue


class RegistweWindowProcess(WindowProcessWithoutQueue):
    def __init__(self, data, RQ, MQ, bet):
        WindowProcessWithoutQueue.__init__(self, data, RQ, MQ, bet, RegisterWindow(self))
        self.title_rect = (0, 0, 650, 100)

    def doAction(self, action):
        if action.type == ActionType.REGISTER:
            bg = self.window.bg
            username = bg.usernameInputbox.text
            password = bg.passwordInputbox.text
            nickname = bg.nicknameInputbox.text
            self.register(username, password, nickname)
            return

    def register(self, username, password, nickname):
        request = {
            'messageNumber': '3',
            'username': username,
            'password': password,
            'nickname': nickname,
            'avatarAddress': 'cd37c244-6558-42de-8fd4-770f75d1be8e',
            'phoneNumber': '',
            'email': '',
            'occupation': '',
            'location': ''
        }
        self.requestQueue.put(request)
        from time import sleep
        sleep(2)
        self.stop()


def createRegisterWindowProcess(data, RQ, MQ):
    rwp = RegistweWindowProcess(data, RQ, MQ, None)
    rwp.run()
