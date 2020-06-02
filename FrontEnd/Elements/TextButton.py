from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.text_variable import text_variable
import pygame

class TextButton(Element):
    # 0 == idle
    # 1 == hover
    # 2 == select
    image = pygame.Surface((100, 100))
    image_hover = pygame.Surface((100, 100))
    image_select = pygame.Surface((100, 100))
    image.fill((85, 165, 255))
    image_hover.fill((105, 185, 255))
    image_select.fill((65, 145, 255))

    def __init__(self, process, location, text, fontsize, size):
        Element.__init__(self, process)
        self.font = pygame.font.SysFont('simhei',fontsize)
        self.content = self.font.render(text,True,(255,255,255))
        # 一般情况下字号对应的宽度为字号的一半，高度为字号原本大小
        self.textWidth = len(text.encode("gbk"))*fontsize/2
        self.textHeight = fontsize
        self.size = size
        self.conPosition = ((size[0]-self.textWidth)/2,(size[1]-self.textHeight)/2)

        self.image = pygame.transform.smoothscale(self.image, size)
        self.image_hover = pygame.transform.smoothscale(self.image_hover, size)
        self.image_select = pygame.transform.smoothscale(self.image_select, size)
        self.location = location
        self.state = 0

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] <= x <= self.location[0] + self.size[0] \
                and self.location[1] <= y <= self.location[1] + self.size[1]:
            return True
        return False

    def getEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.state != 2:
                if self.pos_in(event.pos):
                    self.state = 1
                else:
                    self.state = 0
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.pos_in(event.pos):
                if self.state != 2:
                    self.state = 2
                else:
                    self.state = 1
            else:
                self.state = 0

    def display(self):
        if self.state == 0:
            self.surface = self.image
        elif self.state == 1:
            self.surface = self.image_hover
        else:
            self.surface = self.image_select
        surface = self.surface.copy()
        surface.blit(self.content,self.conPosition)
        return surface
