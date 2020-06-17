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
        # 拖拽后直接发送图片到会话中
        if len(urls)>=1 and urls[0]!=None:
            request = {
                'messageNumber':'9',
                'sessionId':self.process.sessionID,
                    'content':{
                        'from':self.bg.username,
                        'to':None,
                        'time':None,
                        'content':urls[0],
                        'kind':'1',
                    }
            }
            print(request)
            # self.process.requestQueue.put(request)

    
    def __init__(self,process):
        Window.__init__(self,process,'Untitled',(900,750),(255,255,255),True)
        # 从自己的process中获取id，然后在background中获取完整session
        pygame.display.set_caption('Session:'+str(self.process.sessionID))
        self.set_rounded_rectangle(10)
        self.bg = self.createChild(SessionWindowBackground)
        self.setDragFilesCallback(self.DragFilesCallback)

    # session是否需要获取消息进行处理？好像不用
    def getMessage(self,message):
        self.bg.getMessage(message)