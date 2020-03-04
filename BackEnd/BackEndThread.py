from threading import Thread
from queue import Queue
class BackEndThread(Thread):
    def __init__(self,requestQueue,messageQueue):
        Thread.__init__(self)
        self.requestQueue = requestQueue
        self.messageQueue = messageQueue
        self.go = True
    def run(self):
        #Create TCP socket
        while self.go:        
            #self.requestQueue.get()    
            #self.messageQueue.push(message)
            pass
    def stop(self):
        self.go = False
    #@Static methods
    #def saveFile()