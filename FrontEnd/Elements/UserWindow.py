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

        # 获取好友列表
        try:
            if message['messageNumber'] == '4r':
                data['friendList'] = message['friendlist']
                writeData(self.process.data, data)
                self.bg.friend_list.refresh()
                return
        except KeyError:
            print('key error in 20r')

        # 按昵称搜好友
        try:
            if message['messageNumber'] == '20r':
                data['search_nickname'] = message['userlist']
                writeData(self.process.data, data)
                return
        except KeyError:
            print('key error in 20r')

        # 按用户名搜好友
        try:
            if message['messageNumber'] == '21r':
                data['search_username'] = message['userlist']
                writeData(self.process.data, data)
        except KeyError:
            print('key error in 21r')
