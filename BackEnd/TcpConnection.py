from socket import *
import threading
import time

HOST = '127.0.0.1'
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
                msg = self.tcpClientSocket.recv(BUFSIZE)
                msglist.insert(0,msg)
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