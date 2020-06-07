import threading
import json
import pickle
from BackEnd.TcpConnection import TcpClient


# from TcpConnection import TcpClient


class Login(threading.Thread):
    # 登录
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.username = request.get('messageField1', None)
        if self.username is None:
            self.username = request.get('username', None)
        self.password = request.get('messageField2', None)
        if self.password is None:
            self.password = request.get('password', None)

    def run(self):
        data = {'messageField1': self.username, 'messageField2': self.password, 'messageNumber': '2'}
        self.client.sendMessage(data)


class Register(threading.Thread):
    # 注册
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.user = request.get('messageField1', None)
        if self.user is None:
            self.user = {
                'username': request.get('username', None),
                'password': request.get('password', None),
                'avatarAddress': request.get('avatarAddress', None),
                'phoneNumber': request.get('phoneNumber', None),
                'email':request.get('email', None),
                'occupation': request.get('occupation', None),
                'location': request.get('location', None)
            }

    def run(self):
        data = {'messageField1': self.user, 'messageNumber': '3'}
        self.client.sendMessage(data)


class GetFriendList(threading.Thread):
    # 获取好友列表
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        data = {'messageNumber': '4'}
        self.client.sendMessage(data)


class GetHistory(threading.Thread):
    # 获取历史记录
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        data = {'messageNumber': '5'}
        self.client.sendMessage(data)


class CreateSession(threading.Thread):
    # 创建群聊
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        data = {'messageNumber': '6'}
        self.client.sendMessage(data)


class JoinSession(threading.Thread):
    # 加入群聊
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.username = request.get('messageField1', None)
        if self.username is None:
            self.username = request.get('username', None)
        self.sessionId = request.get('messageField2', None)
        if self.sessionId is None:
            self.sessionId = request.get('sessionId')
            if self.sessionId is None:
                self.sessionId = request.get('sessionID')

    def run(self):
        data = {'messageField1': self.username, 'messageField2': self.sessionId, 'messageNumber': '7'}
        self.client.sendMessage(data)


class GetFriendRegister(threading.Thread):
    # 获取好友请求列表
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        data = {'messageNumber': '8'}
        self.client.sendMessage(data)


class SendMessage(threading.Thread):
    # 发送消息
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.sessionId = request.get('messageField1', None)
        if self.sessionId is None:
            self.sessionId = request.get('sessionId', None)
            if self.sessionId is None:
                self.sessionId = request.get('sessionID')
        self.message = request.get('messageField2', None)
        if self.message is None:
            self.message = request.get('message', None)

    def run(self):
        data = {'messageField1': self.sessionId, 'messageField2': self.message, 'messageNumber': '9'}
        self.client.sendMessage(data)


class FriendRegister(threading.Thread):
    # 添加好友
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.toUsername = request.get('messageField1', None)
        if self.toUsername is None:
            self.toUsername = request.get('toUsername', None)
        self.checkMessage = request.get('messageField2', None)
        if self.checkMessage is None:
            self.checkMessage = request.get('checkMessage', None)

    def run(self):
        data = {'messageField1': self.toUsername, 'messageField2': self.checkMessage,
                'messageNumber': '10'}
        self.client.sendMessage(data)


class RespondFriendRegister(threading.Thread):
    # 回应好友申请
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.fromUsername = request.get('messageField1', None)
        if self.fromUsername is None:
            self.fromUsername = request.get('fromUsername', None)
        self.result = request.get('messageField2', None)
        if self.result is None:
            self.result = request.get('result', None)

    def run(self):
        data = {'messageField1': self.fromUsername, 'messageField2': self.result,
                'messageNumber': '12'}
        self.client.sendMessage(data)


class GetFriendRegisterResultList(threading.Thread):
    # 获取好友申请结果列表
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        data = {'messageNumber': '14'}
        self.client.sendMessage(data)


class DeleteFriend(threading.Thread):
    # 删除好友
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.deleteUsername = request.get('messageField1', None)
        if self.deleteUsername is None:
            self.deleteUsername = request.get('deleteUsername', None)

    def run(self):
        data = {'messageField1': self.deleteUsername,
                'messageNumber': '15'}
        self.client.sendMessage(data)


class Close(threading.Thread):
    # 退出登录
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        data = {'messageNumber': '0'}
        self.client.sendMessage(data)
