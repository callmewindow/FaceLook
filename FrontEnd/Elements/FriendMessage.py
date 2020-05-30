from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.text_variable import text_variable
import pygame

class FriendMessage(Element):
    pygame.font.init()

    bg = pygame.Surface((300, 40))
    bg.fill((255, 255, 255))

    def __init__(self, process, location, userId, content):
        Element.__init__(self, process)
        self.location = location
        self.surface = FriendMessage.bg
        self.font = pygame.font.SysFont('simhei', fontsize)
        # 消息头部

        # 消息内容


    def display(self):
        surface = self.surface.copy()
        
        return surface
