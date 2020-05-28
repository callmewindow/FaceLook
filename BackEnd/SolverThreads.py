import threading
import json
import pickle
from TcpConnection import TcpClient


class Login(threading.Thread):
    # 登录
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.username = request['messageField1']
        self.password = request['messageField2']

    def run(self):
        data = {'messageField1':self.username,'messageField2':self.password,'messageNumber':'2'}
        self.client.sendMessage(data)



class Register(threading.Thread):
    # 注册
    def __init__(self, client, request):
        threading.Thread.__init__(self)
        self.client = client
        self.username = request['messageField1']
        self.password = request['messageField2']
        self.nickname = request['messageField3']

    def run(self):
        data = {'messageField1':self.username,'messageField2':self.password,'messageField3':self.nickname,'messageNumber':'3'}
        self.client.sendMessage(data)


class FriendRegister(threading.Thread):
    # 添加好友
    pass


class GetFriendList(threading.Thread):
    # 获取好友列表
    pass


class SendMessage(threading.Thread):
    # 发送消息
    pass


class GetHistory(threading.Thread):
    # 获取历史记录
    pass


class CreateGroup(threading.Thread):
    # 创建群聊
    pass


class JoinChat(threading.Thread):
    # 加入群聊
    pass


class RefreshRecord(threading.Thread):
    # 刷新聊天记录
    pass
