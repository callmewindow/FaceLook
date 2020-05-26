import pygame

pygame.init()
pygame.font.init()
pygame.key.set_repeat()

from FrontEnd.Processes.UserWindowProcess import UserWindowProcess as UWP
from FrontEnd.Processes.LoginWindowProcess import LoginWindowProcess as LWP
from BackEnd.BackEndThread import BackEndThread
from multiprocessing import Process
from Common.base import *

if __name__ == '__main__':
    
    bet = BackEndThread(data, RQ, MQ)
    bet.start()
    # login

    lwp = LWP(data, RQ, MQ, bet)
    # print(bet.messageQueue)
    # print(lwp.messageQueue)
    lwp.run()

    FETEXT(data)
    uwp = UWP(data, RQ, MQ, bet)
    uwp.run()
    bet.stop()
