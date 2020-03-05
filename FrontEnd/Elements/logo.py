from FrontEnd.Elements.Element import Element
import pygame
class logo(Element):
    image = pygame.transform.scale(pygame.image.load('./resources/logo/logo.png'),(400,80))
    def __init__(self,process,location):
        Element.__init__(self,process)
        self.surface = logo.image
        self.surface.set_alpha(0)
        self.location = location

    def update(self):
        if self.state == 1:
            return        
        self.counter += 1
        if self.counter == 255:
            self.state = 1
            return
        self.surface.set_alpha(self.counter)
        print(self.counter)

