import pygame
from FrontEnd.Elements.UserWindow import UserWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from FrontEnd.Processes.SessionWindowProcess import createSession
from FrontEnd.Processes.SearchWindowProcess import createSearch
import multiprocessing
from FrontEnd.Processes.UserInforWindowProcess import createUserInfor
from FrontEnd.Processes.FriendApplyWindowProcess import createFriendApplyProcess


class UserWindowProcess(WindowProcess):
    def __init__(self, data, RQ, MQ, bet):
        self.data = data
        self.bet = bet
        WindowProcess.__init__(self, data, RQ, MQ, bet, UserWindow(self))
        self.sessions = []

    def createSessionWindow(self, sessionID):
        proc = multiprocessing.Process(target=createSession,
                                       args=(sessionID, self.data, self.requestQueue, self.messageQueue))
        proc.start()

    def createSearchWindow(self):
        proc = multiprocessing.Process(target=createSearch,
                                       args=(self.data, self.requestQueue, self.messageQueue))
        proc.start()

    def createInfoWindow(self, user):
        proc = multiprocessing.Process(target=createUserInfor,
                                       args=(user, self.data, self.requestQueue, self.messageQueue))
        proc.start()

    def createFriendApplyWindow(self):
        # 在打开窗口前发送请求拿数据
        request = {
            'messageNumber': '14',
        }
        self.requestQueue.put(request)
        request = {
            'messageNumber': '8',
        }
        self.requestQueue.put(request)

        proc = multiprocessing.Process(target=createFriendApplyProcess,
                                       args=(self.data, self.requestQueue, self.messageQueue))
        proc.start()
