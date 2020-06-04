from FrontEnd.Elements.Window import Window
from FrontEnd.UnitTest.UnitTestBackground import UnitTestBackground as UTB
import pygame
from Common.base import *
class UnitTestWindow(Window):
    def DragFilesCallback(self,msg):
        print('在这里拖放文件{}是无效的。'.format(msg))
    def __init__(self,process):
        Window.__init__(self,process,'UnitTest',(600,450),(255,255,255))
        self.bg = self.createChild(UTB)
        self.setDragFilesCallback(self.DragFilesCallback)
    def getMessage(self,message):
        self.bg.getMessage(message)