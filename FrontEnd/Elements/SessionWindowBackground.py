import pygame
from FrontEnd.Elements.Element import Element
from Common.base import Session
from FrontEnd.Elements.TextArea import TextArea
class MessageList(Element):
    pass
class SessionWindowBackground(Element):
    def __init__(self,process):
        Element.__init__(self,process)
        self.location = (0,0)
        self.surface = pygame.Surface((800,500))
        self.surface.fill((255,255,255))
        self.createChild(TextArea,(100,100),'窗外的麻雀在电线杆上多嘴你说这一句很有夏天的感觉手中的铅笔在纸上来来回回我用几行字形容你是我的谁',(0,0,0))
        #aqua = self.createChild(Aqua,(450,300))

        # 渲染整体框架

        # 渲染按钮部分


    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def update(self):
        for child in self.childs:
            if child.active:
                child.update()
    
        
        
        
        
