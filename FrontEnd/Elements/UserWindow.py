from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.UserWindowBackground import UserWindowBackground
from Common.base import readData, writeData


class UserWindow(Window):
    def __init__(self, process):
        Window.__init__(self, process, 'FaceLook!', (350, 740), (255, 255, 255), True)
        self.bg = self.createChild(UserWindowBackground)
        self.set_rounded_rectangle(20)

    def getMessage(self, message):
        data = readData(self.process.data)

        # 登录
        try:
            if message['messageNumber'] == '2r':
                data['user'] = message['user']
                writeData(self.process.data, data)
                return
        except KeyError:
            print('key error in 2r')

        try:
            if message['messageNumber'] == '20r':
                data['search_nickname'] = message['userlist']
                writeData(self.process.data, data)
                return
        except KeyError:
            print('key error in 20r')

        try:
            if message['messageNumber'] == '21r':
                data['search_username'] = message['userlist']
                writeData(self.process.data, data)
        except KeyError:
            print('key error in 21r')
