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
        #BackEnd.fetchImage(url)
    def update(self):
        if self.ready == True:
            return
        else:
            if self.called == False and self.url:
                ImageManagement.downloadImage(self.url)
                self.called = True
                return
            if self.counter == 0:
                try:
                    localURL = self.url
                    image = pygame.image.load(localURL)
                    self.surface = pygame.transform.smoothscale(image,self.size)
                    del image
                    self.ready = True
                except:
                    return
            else:
                self.counter = (self.counter+1)%60
    def display(self):
        return self.surface
