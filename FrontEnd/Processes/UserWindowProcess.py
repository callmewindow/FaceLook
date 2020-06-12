import pygame
from FrontEnd.Elements.UserWindow import UserWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from FrontEnd.Processes.SessionWindowProcess import createSession
from FrontEnd.Processes.SearchWindowProcess import createSearch
import multiprocessing
from FrontEnd.Processes.UserInforWindowProcess import createUserInfor


class UserWindowProcess(WindowProcess):
    def __init__(self, data, RQ, MQ, bet):
        self.data = data
        WindowProcess.__init__(self, data, RQ, MQ, bet, UserWindow(self))
        self.sessions = []

    def createSessionWindow(self, sessionID):
        # proc = multiprocessing.Process(target=createSession,
        #                                args=(sessionID, self.data, self.requestQueue, self.messageQueue))
        # proc.start()
        proc = multiprocessing.Process(target=createUserInfor,
                                       args=(None, self.data, self.requestQueue, self.messageQueue))
        proc.start()

    def createSearchWindow(self):
        proc = multiprocessing.Process(target=createSearch,
                                       args=(self.data, self.requestQueue, self.messageQueue))
        proc.start()
