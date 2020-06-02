import threading 
import queue
from queue import Queue
from time import sleep
from BackEnd.SolverThreads import *
#from SolverThreads import *

def init(rq):
    # 初始化，创建TCP连接
    client = TcpClient()
    client.runTcp(rq)
    return client


class RequestType():
    INIT = '1'
    LOGIN = '2'
    LOGINRET = '2r'
    REGISTER = '3'
    REGISTERRET = '3r'
    GETFRIENDLIST = '4'
    GETFRIENDLISTRET = '4r'
    GETHISTORY = '5'
    GETHISTORYRET = '5r'

    CREATEGROUP = '6'
    CREATEGROUPRET = '6r'
    JOINCHAT = '7'
    JOINCHATRET = '7r'
    REFRESHRECORD = '8'
    REFRESHRECORDRET = '8r'
    SENDMESSAGE = '9'

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

    CREATEGROUPRET = '6r'
    JOINCHATRET = '7r'
    REFRESHRECORDRET = '8r'

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
        self.task = []

    def run(self):
        self.client = init(self.requestQueue)
        sleep(1)
        #logintest =  {"messageField1": "huangchangzhou", "messageField2": "123456", "messageNumber": "2"}
        #self.requestQueue.put(logintest)
        while self.go:
            request = None
            try:
                request = self.requestQueue.get(block=False)
                print('this request:'+request)
            except:
                pass
            if request is not None:
                self.handleRequest(request)
            sleep(0.1)

    def handleRequest(self, request):
        messageNumber = request.get('messageNumber',None)
        if messageNumber == RequestType.INIT:
            print("连接已建立")
        elif messageNumber == RequestType.LOGIN:
            thread = Login(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.LOGINRET:
            message = {
                'messageNumber':MessageType.LOGINRET,
                'result':request.get('messageField1',None),
                'information':request.get('messageField2',None)
            }
            self.messageQueue.put(message)
        elif messageNumber == RequestType.REGISTER:
            thread = Register(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.REGISTERRET:
            message = {
                'messageNumber':MessageType.REGISTERRET,
                'result':request.get('messageField1',None),
                'information':request.get('messageField2',None)
            }
            self.messageQueue.put(message)
        elif messageNumber == RequestType.CREATEGROUP:
            thread = CreateGroup(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.CREATEGROUPRET:
            message = {
                'messageNumber': MessageType.CREATEGROUPRET,
                'result': request.get('messageField1', None),
                'information':request.get('messageField2', None)
            }
        elif messageNumber == RequestType.JOINCHAT:
            thread = JoinChat(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.JOINCHATRET:
            message = {
                'messageNumber': MessageType.JOINCHATRET,
                'result':request.get('messageField1', None),
                'information':request.get('messageField2', None)
            }
        elif messageNumber == RequestType.REFRESHRECORD:
            thread = RefreshRecord(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.REFRESHRECORDRET:
            message = {
                'messageNumber': MessageType.REFRESHRECORDRET,
                'messages':request.get('messageField1', None)
            }
        elif messageNumber == RequestType.SENDMESSAGE:
            thread = SendMessage(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
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

# requestQueue = queue.Queue()
# messageQueue = queue.Queue()
# backend = BackEndThread(requestQueue,messageQueue)
# backend.start()
# sleep(5)
# backend.stop()
# backend.join()