from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.FriendApplyWindowBackground import FriendApplyWindowBackground
import pygame
from Common.base import *
import sys


class FriendApplyWindow(Window):

    # 拖拽图片
    def DragFilesCallback(self, filePaths):
        print('在这里拖放文件{}是无效的。'.format(filePaths))

    def __init__(self, process):
        # True：生成无边框的窗口
        Window.__init__(self, process, '好友验证', (750, 800), (255, 255, 255), True)

        # set_rounded_rectangle：使用窗口圆角
        self.set_rounded_rectangle(10)

        self.bg = self.createChild(FriendApplyWindowBackground)

        # 拖拽图片
        self.setDragFilesCallback(self.DragFilesCallback)


    def getMessage(self, message):
        self.bg.getMessage(message)