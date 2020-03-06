from threading import Thread
from queue import Queue
from time import sleep
from Common.base import *
class BackEndThread(Thread):
    def __init__(self,data,requestQueue,messageQueue):
        Thread.__init__(self)
        self.data = data
        self.requestQueue = requestQueue
        self.messageQueue = messageQueue
        self.go = True
    def run(self):
        
        while self.go:
            request = None
            try:
                request = self.requestQueue.get(block=False)
            except:
                pass
            if request != None:
                self.doRequest(request)
            sleep(1)
    def doRequest(self,request):
        sleep(1)
        self.messageQueue.put(Message(MessageType.LOGIN,'Test'))
        print('Message PUT')
        print(self.messageQueue.empty())
    def stop(self):
        self.go = False
    