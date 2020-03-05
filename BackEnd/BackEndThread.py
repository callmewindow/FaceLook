from threading import Thread
from queue import Queue
class BackEndThread(Thread):
    def __init__(self,data,requestQueue,messageQueue):
        Thread.__init__(self)
        self.data = data
        self.requestQueue = requestQueue
        self.messageQueue = messageQueue
        self.go = True
    def run(self):
        #Create TCP socket
        while self.go:
            request = None
            try:
                request = self.requestQueue.get(block=False)
            except:
                pass
            if request != None:
                self.doRequest(request)
    def doRequest(self,request):
        #createThread
        pass
    def stop(self):
        self.go = False
    