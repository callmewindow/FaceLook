import pygame
pygame.init()
pygame.key.set_repeat(500, 40)

from FrontEnd.UnitTest.UnitTestProcess import UnitTestProcess as UTP
from Common.base import *
from multiprocessing.managers import BaseManager
def fill_unit_test_data(data):
    pass
    
if __name__ == '__main__':

    manager = BaseManager()
    manager.register('DataCenter',DataCenter)
    manager.start()
    data = manager.DataCenter()
    
    fill_unit_test_data(data)

 
    utp = UTP(data, None, None, data)

    utp.run()

