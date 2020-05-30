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
    
        
        
        
        
