import threading 
import queue
from time import sleep
from BackEnd.SolverThreads import *
from BackEnd.LocalStorage import *
#from SolverThreads import *
#from LocalStorage import *

def init(rq):
    # 初始化，创建TCP连接
    client = TcpClient()
    client.runTcp(rq)
    return client


class RequestType():
    CLOSE = '0'
    INIT = '1r'
    LOGIN = '2'
    LOGINRET = '2r'
    REGISTER = '3'
    REGISTERRET = '3r'
    GETFRIENDLIST = '4'
    GETFRIENDLISTRET = '4r'
    GETHISTORY = '5'
    GETHISTORYRET = '5r'

    CREATESESSION = '6'
    CREATESESSIONRET = '6r'
    JOINSESSION = '7'
    JOINSESSIONRET = '7r'
    REFRESHRECORD = '8'
    REFRESHRECORDRET = '8r'
    SENDMESSAGE = '9'
    SENDMESSAGERET = '9r'

    FRIENDREGISTER = '10'
    FRIENDREGISTERRET = '10r'
    RECEIVEFRIENDREGISTERRET = '11r'
    RESPONDFRIENDREGISTER = '12'
    RESPONDFRIENDREGISTERRET = '12r'
    DELETEFRIEND = '13'
    DELETEFRIENDRET = '13r'



class MessageType():
    LOGINRET = '2r'
    REGISTERRET = '3r'
    GETFRIENDLISTRET = '4r'

    CREATESESSIONRET = '6r'
    JOINSESSIONRET = '7r'
    REFRESHRECORDRET = '8r'
    SENDMESSAGERET = '9r'

    FRIENDREGISTERRET = '10r'
    RECEIVEFRIENDREGISTERRET = '11r'
    RESPONDFRIENDREGISTERRET = '12r'
    DELETEFRIENDRET = '13r'


class BackEndThread(threading.Thread):
    def __init__(self, requestQueue, messageQueue):
        threading.Thread.__init__(self)
        self.requestQueue = requestQueue
        self.messageQueue = messageQueue
        self.threadList = list()
        self.go = True
        self.client = None
        self.username = None
        self.localStorage = None
        self.task = []

    def run(self):
        self.client = init(self.requestQueue)
        sleep(1)

        while self.go:
            request = None
            try:
                request = self.requestQueue.get(block=False)
                print('this request:',request)
            except:
                pass
            if request is not None:
                self.handleRequest(request)
            sleep(0.1)

    def handleRequest(self, request):
        messageNumber = request.get('messageNumber',None)
        if messageNumber == RequestType.INIT:
            print("连接已建立")
        #退出登录
        #request格式：{"messageNumber": "0"}
        elif messageNumber == RequestType.CLOSE:
            thread = Close(self.client)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        #登录
        #request格式：{"username": "hcz", "password": "123456", "messageNumber": "2"}
        #message格式：见下方
        elif messageNumber == RequestType.LOGIN:
            thread = Login(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.LOGINRET:
            result = request.get('messageField1',None)
            message = {
                'messageNumber':MessageType.LOGINRET,
                'result':result,
                'information':request.get('messageField2',None)
            }
            self.messageQueue.put(message)
            self.username = request.get('messageField3',None)
            print(type(result))
            if result != 0 and self.username != None:
                self.localStorage = LocalStorage(self.username)
        #注册
        #request格式：{"username": "hcz", "password": "123456", "nickname": "quq", "messageNumber": "2"}
        #message格式：见下方
        elif messageNumber == RequestType.REGISTER:
            thread = Register(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.REGISTERRET:
            result = request.get('messageField1',None)
            message = {
                'messageNumber':MessageType.REGISTERRET,
                'result':request.get('messageField1',None),
                'information':request.get('messageField2',None)
            }
            self.messageQueue.put(message)
            self.username = request.get('messageField3',None)
            if result != 0 and self.username != None:
                self.localStorage = LocalStorage(self.username)
        #获取好友列表
        #request格式：{"messageNumber": "4"}
        #message格式：num表示好友个数，friendlist为一个dict列表，字段分别为username和nickname
        elif messageNumber == RequestType.GETFRIENDLIST:
            thread = GetFriendList(self.client)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.GETFRIENDLISTRET:
            friendlist = request.get('content',None)
            if friendlist == None or type(friendlist) != list:
                self.requestFailure()
                return
            num = len(friendlist)
            result = []
            temp = {}
            for friend in friendlist:
                temp['username'] = friend.get('messageField1')
                temp['nickname'] = friend.get('messageField2')
                result.append(temp)
            message = {
                'messageNumber':MessageType.GETFRIENDLISTRET,
                'num' : num,
                'friendlist' : result
            }
            self.messageQueue.put(message)
        #获取历史消息
        #未实装
        elif messageNumber == RequestType.GETHISTORY:
            thread = GetHistory(self.client)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.GETHISTORYRET:
            pass
        #建立会话并自动加入
        #request格式：{"messageNumber": "6"}
        #message格式：sessionID若为0则表示建立失败
        elif messageNumber == RequestType.CREATESESSION:
            thread = CreateSession(self.client)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.CREATESESSIONRET:
            sessionID = request.get('messageField1', None)
            message = {
                'messageNumber': MessageType.CREATESESSIONRET,
                'sessionID': sessionID
            }
            self.messageQueue.put(message)
            if sessionID != 0 and self.localStorage != None:
                self.localStorage.addSession(sessionID)
        #邀请他人加入会话
        #request格式：{"messageNumber": "7","username":"dsm","sessionId":"2"}   (sessionID也可兼容)
        #message格式：见下方
        elif messageNumber == RequestType.JOINSESSION:
            thread = JoinSession(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.JOINSESSIONRET:
            message = {
                'messageNumber': MessageType.JOINSESSIONRET,
                'result':request.get('messageField1', None),
                'information':request.get('messageField2', None)
            }
            self.messageQueue.put(message)
        # #刷新历史记录（已废除）
        # elif messageNumber == RequestType.REFRESHRECORD:
        #     thread = RefreshRecord(self.client, request)
        #     thread.setDaemon(True)
        #     thread.start()
        #     self.task.append(thread)
        # elif messageNumber == RequestType.REFRESHRECORDRET:
        #     message = {
        #         'messageNumber': MessageType.REFRESHRECORDRET,
        #         'messages':request.get('messageField1', None)
        #     }

        #发送/接收消息
        # request使用eg：注意时间格式
        # message = {'from':'hcz','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),'content':'hello dsm'}
        # request = {"messageNumber": "9",'sessionID':'2','message':json.dumps(message)} 
        # message格式：见下方，message为一个dict
        elif messageNumber == RequestType.SENDMESSAGE:
            thread = SendMessage(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
            sessionID = request.get('messageField1', None)
            if sessionID == None:
                sessionID = request.get('sessionId',None)
                if sessionID == None:
                    sessionID == request.get('sessionID')
            message = request.get('messageField2', None)
            if message == None:
                message = request.get('message',None)
            if message != None:
                content = json.loads(message)
            self.localStorage.addRecordsDict(sessionID,content)

        elif messageNumber == RequestType.SENDMESSAGERET:
            data = request.get('messageField2', None)
            if data != None:
                content = json.loads(data)
            sessionID = request.get('messageField1', None)
            message = {
                'messageNumber': MessageType.SENDMESSAGERET,
                'sessionId' : sessionID,
                'message' : content
            }
            self.messageQueue.put(message)
            self.localStorage.addRecordsDict(sessionID,content)

        #以下未实装

        #添加好友
        elif messageNumber == RequestType.FRIENDREGISTER:
            thread = FriendRegister(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.FRIENDREGISTERRET:
            message = {
                'messageNumber': MessageType.FRIENDREGISTERRET,
                'result': request.get('messageField1',None),
                'information': request.get('messageField2',None)
            }
            self.messageQueue.put(message)
        #收到好友申请
        elif messageNumber == RequestType.RECEIVEFRIENDREGISTERRET:
            message = {
                'messageNumber': MessageType.RECEIVEFRIENDREGISTERRET,
                'fromUsername': request.get('messageField1',None),
                'message': request.get('messageField2',None)
            }
            self.messageQueue.put(message)
        elif messageNumber == RequestType.RESPONDFRIENDREGISTER:
            thread = RespondFriendRegister(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        #回复申请
        elif messageNumber == RequestType.RESPONDFRIENDREGISTERRET:
            message = {
                'messageNumber': MessageType.RESPONDFRIENDREGISTERRET,
                'result': request.get('messageField1',None),
                'information': request.get('messageField2',None)
            }
            self.messageQueue.put(message)
        elif messageNumber == RequestType.DELETEFRIEND:
            thread = DeleteFriend(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        #删除好友
        elif messageNumber == RequestType.DELETEFRIENDRET:
            message = {
                'messageNumber': MessageType.DELETEFRIENDRET,
                'result': request.get('messageField1',None),
                'information': request.get('messageField2',None)
            }
            self.messageQueue.put(message)
        else:
            self.stop()
        
    def stop(self):
        for tk in self.task:
            tk.join(timeout = 1)
        if self.client is not None:
            self.client.closeServer()
        else:
            print("尚未建立连接")
        self.go = False
        if self.localStorage != None:
            self.localStorage.close()

    def requestFailure(self):
        pass