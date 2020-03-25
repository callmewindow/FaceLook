from socket import *
import threading
import json
import pickle
import time

HOST = '175.24.10.214'
PORT = 9000
BUFSIZE = 1024
ADDRESS = (HOST, PORT)

class TcpClient(object):
    def __init__(self):
        self.tcpClientSocket = socket(AF_INET, SOCK_STREAM)
        self.stopFlag = False

    def receiverThread(self,msglist):
        while (self.stopFlag == False):
            try:
                #如果运行到此处isStop的值改变，能否退出循环，此处存疑
                self.datap = self.tcpClientSocket.recv(BUFSIZE)
                self.dataj = pickle.loads(self.datap)
                self.data = json.loads(self.dataj)
                msglist.put(self.data)
            except error as e:
                if(e.errno == 1):
                    time.sleep(0.5)

    def run(self,msglist):
        self.tcpClientSocket.connect(ADDRESS)
        self.tcpClientSocket.setblocking(0)
        self.receiver = threading.Thread(target=TcpClient.receiverThread,args=(self,msglist))
        self.receiver.start()

    def sendMessage(self,msg):
        self.tcpClientSocket.send(msg)
    
    def closeServer(self):
        self.stopFlag = True
        self.receiver.join()
        self.tcpClientSocket.close()