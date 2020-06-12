from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.UserInforWindowBackground import UserInforWindowBackground
import pygame
from Common.base import *
import sys

class UserInforWindow(Window):
    def DragFilesCallback(self,msg):
        # 图片上传倒了
        urls = []
        print(msg)
        for fp in msg:
            url = ImageManagement.uploadImage(fp)
            urls.append(url)
            print(url)
        if len(urls)>=1 and urls[0]!=None:
            self.bg.avatar.url = urls[0]

    def __init__(self,process):
        Window.__init__(self,process,'个人信息',(500,600),(63, 115, 163),True)
        self.bg = self.createChild(UserInforWindowBackground)
        self.set_rounded_rectangle(10)
        self.setDragFilesCallback(self.DragFilesCallback)
    
    def getMessage(self,message):
        self.bg.getMessage(message)