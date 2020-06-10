from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.GroupInforWindowBackground import GroupInforWindowBackground
import pygame
from Common.base import *
import sys

class GroupInforWindow(Window):
    def DragFilesCallback(self,msg):
        urls = []
        for fp in msg:
            url = ImageManagement.uploadImage(fp)
            urls.append(url)
            print(url)
        # if len(urls)>=1 and urls[0]!=None:
        #     self.bg.testImage.url = urls[0]

    def __init__(self,process):
        Window.__init__(self,process,'群聊信息',(400,500),(63, 115, 163),True)
        self.bg = self.createChild(GroupInforWindowBackground)
        self.set_rounded_rectangle(10)
        self.setDragFilesCallback(self.DragFilesCallback)
    
    def getMessage(self,message):
        self.bg.getMessage(message)