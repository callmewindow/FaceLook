from FrontEnd.Elements.Element import Element
import pygame
from BackEnd import ImageManagement


class Image(Element):
    def __init__(self, process, location, size, url):
        Element.__init__(self, process)
        self.location = location
        self.url = url
        self.surface = pygame.Surface(size)
        self.surface.fill((128,128,128))
        self.ready = False
        self.size = size
        self.counter = 0
        self.called = False
    def update(self):
        if self.ready == True:
            return
        #Not Ready
        self.counter = (self.counter+1)%10
        if self.counter == 1 and self.url:
            surface = ImageManagement.getLocalImage('./images/'+self.url)
            if surface != None:
                self.surface = pygame.transform.smoothscale(surface, self.size)
                self.ready = True
                return
            #Not local
            if self.called == False:
                ImageManagement.downloadImage(self.url)
                self.called = True
            else:
                #called and not returned
                pass
            
    def display(self):
        return self.surface
