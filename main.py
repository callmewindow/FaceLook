from FrontEnd.Processes.UserWindowProcess import UserWindowProcess as UWP
from FrontEnd.Processes.LoginWindowProcess import LoginWindowProcess as LWP
from BackEnd.BackEndThread import BackEndThread
from multiprocessing import Process
from Common.base import *
from queue import Queue
import pygame
pygame.init()
pygame.key.set_repeat()
pygame.key.set_text_input_rect(pygame.Rect(0,0,800,800))
if __name__ == '__main__':
    data = DataCenter()
    RQ = Queue()
    MQ = Queue()    
    bet = BackEndThread(data,RQ,MQ)
    bet.start()
    #login
    lwp = LWP(data,RQ,MQ,bet)
    lwp.run()
    bet.stop()
    #uwp = uwp(data,RQ,MQ,bet)
   # uwp.run()
