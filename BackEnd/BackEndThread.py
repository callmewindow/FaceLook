from threading import Thread
class BackEndThread(Thread):
    def __init__(self,messageQueue,data):
        Thread.__init__(self)
        self.messageQueue = messageQueue
        self.data = data
        self.go = True
    def run(self):
        #Create TCP socket
        while self.go:            
            #self.messageQueue.push(message)
            pass
    def stop(self):
        self.go = False
    #@Static methods
    #def saveFile()