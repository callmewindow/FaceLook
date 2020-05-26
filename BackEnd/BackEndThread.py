from threading import Thread
from queue import Queue
from time import sleep
from Common.base import *
from BackEnd.SolverThreads import *

class BackEndThread(Thread):
    def __init__(self,data,requestQueue,messageQueue):
        Thread.__init__(self)
        self.data = data
        self.requestQueue = requestQueue
        self.messageQueue = messageQueue
        self.go = True
        #self.client = init(self.requestQueue)
    def run(self):
        while self.go:
            request = None
            try:
                request = self.requestQueue.get(block=False)
            except:
                pass
            if request != None:
                self.handleRequest(request)
            sleep(1)
    def handleRequest(self,request):
        if request['type'] == 'login':
            username = request['username']
            password = request['password']
            Login(self.client,username,password)
        elif request['type'] == 'loginRet':
            value = request['value']
            data = {'type':'loginRet','result':value}
            self.messageQueue.put(data)
        elif request['type'] == 'register':
            username = request['username']
            password = request['password']
            Register(self.client,username,password)
        elif request['type'] == 'registerRet':
            value = request['value']
            data = {'type':'registerRet','result':value}
            self.messageQueue.put(data)
        else:
            self.stop() 
    def stop(self):
        self.go = False
    