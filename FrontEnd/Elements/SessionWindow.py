from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.SessionWindowBackground import SessionWindowBackground
import pygame
from Common.base import *
import sys

class SessionWindow(Window):
    def DragFilesCallback(self,msg):
        urls = []
        for fp in msg:
            url = ImageManagement.uploadImage(fp)
            urls.append(url)
            print(url)
        # if len(urls)>=1 and urls[0]!=None:
        #     self.bg.testImage.url = urls[0]
    
    def __init__(self,process):
        Window.__init__(self,process,'Untitled',(900,750),(255,255,255),True)
        # 从自己的process中获取id
        pygame.display.set_caption('Session:'+str(self.process.sessionID))
        self.set_rounded_rectangle(10)
        self.bg = self.createChild(SessionWindowBackground)
        self.setDragFilesCallback(self.DragFilesCallback)

    def getMessage(self,message):
        self.bg.getMessage(message)