from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.RegisterWindowBackground import RegisterWindowBackground as RWBG
from Common.base import *
class RegisterWindow(Window):
    def DragFilesCallback(self,filePaths):
        print('在这里拖放文件{}是无效的。'.format(filePaths))


    def __init__(self,process):
        Window.__init__(self,process,'Login',(600,450),(255,255,255),True)
        self.set_rounded_rectangle(40)
        self.bg = self.createChild(RWBG)
        self.setDragFilesCallback(self.DragFilesCallback)
    def getMessage(self,message):
        self.bg.getMessage(message)