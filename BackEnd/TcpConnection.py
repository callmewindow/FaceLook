from socket import *
import threading
import json
import pickle
import time

HOST = '175.24.10.214'
PORT = 21915
BUFSIZE = 1024
ADDRESS = (HOST, PORT)


class TcpClient(object):
    def __init__(self):
        self.tcpClientSocket = socket(AF_INET, SOCK_STREAM)
        self.stopFlag = threading.Event()
        self.receiver = None

    def receiverThread(self, rq, event):
        while not event.isSet():
            try:
                # 如果运行到此处stopFlag的值改变，能否退出循环，此处存疑
                dataj = self.tcpClientSocket.recv(BUFSIZE).decode("utf-8")
                if len(dataj)>0:
                    data = json.loads(dataj)
                    print(data)
                else:
                    continue
                rq.put(data)
            except error as e:
                print(e)

    def runTcp(self, rq):
        try:
            self.tcpClientSocket.connect(ADDRESS)
            self.receiver = threading.Thread(target=TcpClient.receiverThread, args=(self, rq,self.stopFlag))
            self.receiver.start()
        except error as e:
            print(e)

    def sendMessage(self, data):
        # data为dict即可
        try:
            dataj = json.dumps(data)
            self.tcpClientSocket.send(dataj.encode("utf-8"))
        except error as e:
            print(e)

    def closeServer(self):
        self.stopFlag.set()
        if self.receiver is not None:
            self.tcpClientSocket.close()
            self.receiver.join()
        
        
