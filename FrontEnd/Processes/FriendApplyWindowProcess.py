import pygame

from FrontEnd.Elements.FriendApplyWindow import FriendApplyWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from FrontEnd.Processes.WindowProcessWithoutQueue import WindowProcessWithoutQueue

import multiprocessing


class FriendApplyWindowProcess(WindowProcessWithoutQueue):

    def __init__(self, data, RQ, MQ):

        bet = None
        self.data = data
        WindowProcess.__init__(self, data, RQ, MQ, bet, FriendApplyWindow(self))
        self.friend()

    def friend(self):
        request = {
            'messageNumber': '14',
        }
        print('send14msg1')
        self.requestQueue.put(request)
        print('send14msg2')

# 给zyx的UserWindowProcess提供接口
def createFriendApplyProcess(data, RQ, MQ):

    fap = FriendApplyWindowProcess(data, RQ, MQ)
    fap.run()



