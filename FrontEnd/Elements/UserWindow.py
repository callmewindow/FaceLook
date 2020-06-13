from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.UserWindowBackground import UserWindowBackground
from Common.base import readData, writeData
from time import sleep


class UserWindow(Window):
    def __init__(self, process):
        Window.__init__(self, process, 'FaceLook!', (350, 740), (255, 255, 255), True)
        self.bg = self.createChild(UserWindowBackground)
        self.set_rounded_rectangle(20)
        self.need_session = False
        self.needed_username = ''

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
            print('key error in 4r')

        # 创建会话
        try:
            if message['messageNumber'] == '6r':
                if self.need_session:
                    self.need_session = False
                    self.process.requestQueue.put({'messageNumber': '7',
                                                   'username': self.needed_username,
                                                   'sessionId': message['sessionId']})
                    self.process.requestQueue.put({'messageNumber': '5'})
                else:
                    self.process.requestQueue.put({'messageNumber': '5'})
                    sleep(1)
                    self.bg.group_list.refresh()
                return
        except KeyError:
            print('key error in 6r')

        # 获取未处理好友申请列表
        try:
            if message['messageNumber'] == '8r':
                data['friend_apply']['requestorList'] = message['requestorList']
                writeData(self.process.data, data)
                return
        except KeyError:
            print('key error in 8r')

        # 好友申请消息（服务端==>接收方）（仅限接收方在线）
        try:
            if message['messageNumber'] == '11r':
                data['friend_apply']['requestor'] = message
                writeData(self.process.data, data)
                return
        except KeyError:
            print('key error in 11r')

        # 回复好友申请（接收方==>服务端）
        try:
            if message['messageNumber'] == '12r' and message['result'] == 1:
                self.need_session = True
                self.needed_username = message['requestorUsername']
                self.process.requestQueue.put({'messageNumber': '4'})
                return
        except KeyError:
            print('key error in 12r')

        # 好友申请回复结果（服务端==>申请方）（仅限申请方在线）
        try:
            if message['messageNumber'] == '13r':
                data['friend_apply']['receiver'] = message
                writeData(self.process.data, data)
                return
        except KeyError:
            print('key error in 13r')

        # 获取申请结果列表
        try:
            if message['messageNumber'] == '14r':
                data['friend_apply']['receiverList'] = message['receiverList']
                writeData(self.process.data, data)
                return
        except KeyError:
            print('key error in 14r')

        # 删除好友（A==>服务端）
        try:
            if message['messageNumber'] == '15r':
                for i in range(len(data['friendList'])):
                    if data['friendList'][i]['username'] == message['username']:
                        del data['friendList'][i]
                        break
                writeData(self.process.data, data)
                self.bg.friend_list.refresh()
                return
        except KeyError:
            print('key error in 15r')

        # 删除好友（服务端==>B）
        try:
            if message['messageNumber'] == '16r':
                data['friendList'] = message['friendlist']
                writeData(self.process.data, data)
                self.bg.friend_list.refresh()
                return
        except KeyError:
            print('key error in 16r')

        # 更改个人信息
        try:
            if message['messageNumber'] == '18r':
                data['user'] = {
                    'username': data['user']['username'],
                    'nickname': message['nickname'],
                    'avatarAddress': message['avatarAddress'],
                    'phoneNumber': message['phoneNumber'],
                    'invitee': message['invitee'],
                    'email': message['email'],
                    'occupation': message['occupation'],
                    'location': message['location'],
                }
                writeData(self.process.data, data)
                self.bg.self_info.refresh()
                return
        except KeyError:
            print('key error in 18r')

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
