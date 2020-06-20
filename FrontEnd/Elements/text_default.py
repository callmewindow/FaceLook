from Common.base import *
from FrontEnd.Elements.Element import Element
from random import randint
class text_default(Element):
    font = pygame.font.SysFont('simhei',25)
    def __init__(self,process,location,text,color):
        Element.__init__(self,process)
        self.location = location
        self.surface = text_default.font.render(text,True,color)
        self.text = text
        self.color = color
    def alignCenter(self,pos):
        x = pos[0]
        y = pos[1]
        rect = self.surface.get_rect()
        rectX = rect[2]
        rectY = rect[3]
        self.location = (x-rectX//2,y-rectY//2)
    def setText(self,text):
        self.text = text
        rect = self.surface.get_rect()
        self.surface = text_default.font.render(text,True,self.color)        
        rectX = rect[2]
        rectY = rect[3]
        center = (self.location[0]+rectX//2,self.location[1]+rectY//2)
        self.alignCenter(center)
class LoadingText(text_default):
    def __init__(self,process,location,text,color):
        text_default.__init__(self,process,location,text,color)
        
        self.fade_frame = 90
        
        self.texts = ['正在打破次元壁...','正在和hololive争夺版权...','正在致敬bilibili...','正在向腾讯QQ学习...']
        self.setText(self.texts[randint(0,3)]) 
        self.counter = self.fade_frame*2
    def update(self):
        self.counter = (self.counter+1)%(self.fade_frame*3)
        if self.counter<self.fade_frame:
            alpha = 255 * (1-self.counter / self.fade_frame)
            self.surface.set_alpha(alpha)
        elif self.counter == self.fade_frame:            
            self.setText(self.texts[randint(0,3)]) 
            self.surface.set_alpha(0)           
        elif self.counter<=2*self.fade_frame-1:
            alpha = 255 * (self.counter/self.fade_frame-1)
            self.surface.set_alpha(alpha)
        elif self.counter<=3*self.fade_frame-1:
            pass
        else:
            panic('[Fatal Error]LoadingText.counter has unexpected value.')
    def enable(self):
        text_default.enable(self)
        self.counter = 0
    def disable(self):
        text_default.disable(self)
        self.counter = 0
            
    