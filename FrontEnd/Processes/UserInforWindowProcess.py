import pygame
from FrontEnd.Elements.UserInforWindow import UserInforWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from FrontEnd.Processes.SessionWindowProcess import SessionWindowProcess
from FrontEnd.Processes.SessionWindowProcess import createSession
import multiprocessing

class UserInforWindowProcess(WindowProcess):
    def __init__(self,data,RQ,MQ,bet):
        WindowProcess.__init__(self,data,RQ,MQ,bet,UserInforWindow(self))
        self.window.bg.init()
    
    # 打开修改信息窗口
    def createModifyWindow(self,userId,data):
        # 判断修改的对象类型
        if userId == self.uid:
            # 修改自身信息
            pass
        else:
            # 修改好友信息
            pass
    
    # 添加好友
    def addFriend(self,friendId):
        print(friendId)

    # 删除好友
    def deleteFriend(self,friendId):
        print(friendId)

    # 向好友发起会话
    def createSessionWindow(self,sessionID):
        proc = multiprocessing.Process(target=createSession,args=(sessionID,self.data))
        proc.start()
