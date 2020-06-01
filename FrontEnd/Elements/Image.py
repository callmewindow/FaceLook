from FrontEnd.Elements.Element import Element
import pygame


class Image(Element):
    def __init__(self, process, location, size, url):
        Element.__init__(self, process)
        self.location = location
        self.url = url
        self.surface = pygame.surface(size)
        self.surface.fill((0,0,0))
        self.ready = False
        self.size = size
        #BackEnd.fetchImage(url)
    def update(self):
        if self.ready == True:
            return
        else:
            try:
                localURL = self.url
                image = pygame.image.load(localURL)
                self.surface = pygame.transform.smoothscale(image,self.size)
                del image
                self.ready = True
            except:
                return
    def display(self):
        return self.surface
