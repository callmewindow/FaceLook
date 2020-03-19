import threading
import json
import pickle
from BackEnd.TcpConnection import TcpClient

def init(msglist):
    #初始化，创建TCP连接
    client = TcpClient()
    client.run(msglist)
    return client

class Login(threading.Thread):
    #登录
    def __init__(self,client,username,password):
        threading.Thread.__init__(self)
        self.client = client
        self.username = username
        self.password = password
    def run(self):
        self.data = [{ 'username' : self.username, 'password' : self.password}]
        #服务端要求收到字节流，因此需要先转json再序列化
        self.dataj = json.dumps(self.data)
        self.datap = pickle.dumps(self.dataj)
        self.client.sendMessage(self.datap)

class Register(threading.Thread):
    #注册
    def __init__(self,client,username,password):
        threading.Thread.__init__(self)
        self.client = client
        self.username = username
        self.password = password
    def run(self):
        self.data = [{ 'username' : self.username, 'password' : self.password}]
        self.dataj = json.dumps(self.data)
        self.datap = pickle.dumps(self.dataj)
        self.client.sendMessage(self.datap)

class FriendRegister(threading.Thread):
    #添加好友
    pass

class GetFriendList(threading.Thread):
    #获取好友列表
    pass

class SendMessage(threading.Thread):
    #发送消息
    pass

class GetHistory(threading.Thread):
    #获取历史记录
    pass

class CreateGroup(threading.Thread):
    #创建群聊
    pass

class JoinChat(threading.Thread):
    #加入群聊
    pass

class RefreshRecord(threading.Thread):
    #刷新聊天记录
    pass

