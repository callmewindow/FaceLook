from FrontEnd.Processes import UserWindowProcess as UWP
from FrontEnd.Processes import LoginWindowProcess as LWP
from multiprocessing import Process
from Common.DataObject import DataObject
import pygame
pygame.init()
pygame.key.set_repeat()
if __name__ == '__main__':
    data = DataObject()
    #login
    p = Process(target=LWP.main,args=(data,))
    p.start()
    p.join()
    data.login = True
    #main
    #p = Process(target=UWP.main,args=(data,))
    #p.start()
    #p.join()
    #收尾...
