from threading import Thread
from queue import Queue
from time import sleep
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
        print(request.content)
    def stop(self):
        self.go = False
    