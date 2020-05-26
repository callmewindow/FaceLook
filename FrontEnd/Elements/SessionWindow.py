from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.SessionWindowBackground import SessionWindowBackground
import pygame

class SessionWindow(Window):
    def __init__(self,process):
        Window.__init__(self,process,'Untitled',(800,500),(255,255,255))
        pygame.display.set_caption('Session:'+str(self.process.sessionID))
        self.bg = self.createChild(SessionWindowBackground)
