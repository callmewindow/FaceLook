import threading 
import queue
from queue import Queue
from time import sleep
from SolverThreads import *


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


class MessageType():
    LOGINRET = '2r'
    REGISTERRET = '3r'


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
            except:
                pass
            if request is not None:
                self.handleRequest(request)
            sleep(0.1)

    def handleRequest(self, request):
        messageNumber = request['messageNumber']
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
                'result':request['messageField1'],
                'information':request['messageField2']
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
                'result':request['messageField1'],
                'information':request['messageField2']
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