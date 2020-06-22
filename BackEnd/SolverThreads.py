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
                'nickname': request.get('nickname', None),
                'avatarAddress': request.get('avatarAddress', None),
                'phoneNumber': request.get('phoneNumber', None),
                'invitee': request.get('invitee', None),
                'email': request.get('email', None),
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
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.sessionName = request.get('messageField1', None)
        if self.sessionName is None:
            self.sessionName = request.get('sessionName', None)

    def run(self):
        data = {'messageField1': self.sessionName, 'messageNumber': '6'}
        self.client.sendMessage(data)


class JoinSession(threading.Thread):
    # 邀请他人加入会话
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
            self.message = request.get('content', None)

    def run(self):
        data = {'messageField1': self.sessionId, 'messageField2': self.message, 'messageNumber': '9'}
        self.client.sendMessage(data)


class FriendRegister(threading.Thread):
    # 添加好友
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.receiverUsername = request.get('messageField1', None)
        if self.receiverUsername is None:
            self.receiverUsername = request.get('username', None)
        self.checkMessage = request.get('messageField2', None)
        if self.checkMessage is None:
            self.checkMessage = request.get('checkMessage', None)

    def run(self):
        data = {'messageField1': self.receiverUsername, 'messageField2': self.checkMessage,
                'messageNumber': '10'}
        self.client.sendMessage(data)


class RespondFriendRegister(threading.Thread):
    # 回应好友申请
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.requestorUsername = request.get('messageField1', None)
        if self.requestorUsername is None:
            self.requestorUsername = request.get('requestorUsername', None)
        self.result = request.get('messageField2', None)
        if self.result is None:
            self.result = request.get('result', None)

    def run(self):
        data = {'messageField1': self.requestorUsername, 'messageField2': self.result,
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
        self.username = request.get('messageField1', None)
        if self.username is None:
            self.username = request.get('username', None)

    def run(self):
        data = {'messageField1': self.username,
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


class ExitSession(threading.Thread):
    # 退出群聊
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.sessionId = request.get('messageField1', None)
        if self.sessionId is None:
            self.sessionId = request.get('sessionId', None)

    def run(self):
        data = {'messageField1': self.sessionId,
                'messageNumber': '17'}
        self.client.sendMessage(data)


class UpdatePersonalInformation(threading.Thread):
    # 更改个人信息
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.user = request.get('messageField1', None)
        if self.user is None:
            self.user = {
                'username': request.get('username', None),
                'password': request.get('password', None),
                'nickname': request.get('nickname', None),
                'avatarAddress': request.get('avatarAddress', None),
                'phoneNumber': request.get('phoneNumber', None),
                'invitee': request.get('invitee', None),
                'email': request.get('email', None),
                'occupation': request.get('occupation', None),
                'location': request.get('location', None)
            }

    def run(self):
        data = {'messageField1': self.user,
                'messageNumber': '18'}
        self.client.sendMessage(data)


class UpdateSessionInformation(threading.Thread):
    # 修改群聊信息
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.sessionId = request.get('messageField1', None)
        if self.sessionId is None:
            self.sessionId = request.get('sessionId', None)
            if self.sessionId is None:
                self.sessionId = request.get('sessionID', None)
        self.sessionName = request.get('messageField2', None)
        if self.sessionName is None:
            self.sessionName = request.get('sessionName', None)

    def run(self):
        data = {'messageField1': self.sessionId, 'messageField2': self.sessionName,
                'messageNumber': '19'}
        self.client.sendMessage(data)


class SearchByNickname(threading.Thread):
    # 通过nickname搜索
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.nickname = request.get('messageField1', None)
        if self.nickname is None:
            self.nickname = request.get('keyword', None)

    def run(self):
        data = {'messageField1': self.nickname,
                'messageNumber': '20'}
        self.client.sendMessage(data)


class SearchByUsername(threading.Thread):
    # 通过nickname搜索
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.username = request.get('messageField1', None)
        if self.username is None:
            self.username = request.get('keyword', None)

    def run(self):
        data = {'messageField1': self.username,
                'messageNumber': '21'}
        self.client.sendMessage(data)


class KickOut(threading.Thread):
    # 群主踢人
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.sessionId = request.get('messageField1', None)
        if self.sessionId is None:
            self.sessionId = request.get('sessionId', None)
            if self.sessionId is None:
                self.sessionId = request.get('sessionID', None)
        self.username = request.get('messageField2', None)
        if self.username is None:
            self.username = request.get('username', None)

    def run(self):
        data = {'messageField1': self.sessionId, 'messageField2': self.username,
                'messageNumber': '22'}
        self.client.sendMessage(data)