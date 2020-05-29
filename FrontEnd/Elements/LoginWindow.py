from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.LoginWindowBackgrond import LoginWindowBackground as lwb
import pygame
from Common.base import *
class LoginWindow(Window):
    def DragFilesCallback(self,msg):
        print('在这里拖放文件{}是无效的。'.format(msg))
    def __init__(self,process):
        Window.__init__(self,process,'Login',(600,450),(255,255,255))
        self.bg = self.createChild(lwb)
        self.setDragFilesCallback(self.DragFilesCallback)
    def getMessage(self,message):
        self.bg.getMessage(message)