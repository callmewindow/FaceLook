from FrontEnd.Elements.Element import Element
import pygame
class logo(Element):
    image = pygame.transform.scale(pygame.image.load('./resources/logo/logo.png'),(400,80))
    def __init__(self,process,location):
        Element.__init__(self,process)
        self.surface = logo.image.convert()
        self.surface.set_colorkey((255,255,255))
        self.location = location
    '''
    def update(self):
        if self.state == 1:
            return        
        self.counter += 1
        if self.counter == 100:
            self.state = 1
            return
        self.surface.set_alpha(self.counter)
    '''
