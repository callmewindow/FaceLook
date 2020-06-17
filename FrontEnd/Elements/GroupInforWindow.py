from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.GroupInforWindowBackground import GroupInforWindowBackground
import pygame
from Common.base import *
import sys
import win32gui
import win32con

class GroupInforWindow(Window):
    # 群聊没有拖拽的功能
    def __init__(self,process):
        Window.__init__(self,process,'群聊信息',(500,600),(63,115,163),True)
        self.bg = self.createChild(GroupInforWindowBackground)
        self.set_rounded_rectangle(10)