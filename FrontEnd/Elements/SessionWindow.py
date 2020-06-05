from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.SessionWindowBackground import SessionWindowBackground
import pygame
from Common.base import *
import sys

class SessionWindow(Window):
    def DragFilesCallback(self,filePaths):
        print('在这里拖放文件{}是无效的。'.format(filePaths))
    
    def __init__(self,process):
        Window.__init__(self,process,'Untitled',(900,750),(255,255,255),True)
        pygame.display.set_caption('Session:'+str(self.process.sessionID))
        # self.set_rounded_rectangle(10)
        self.bg = self.createChild(SessionWindowBackground)
