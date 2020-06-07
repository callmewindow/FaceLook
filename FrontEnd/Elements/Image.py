from FrontEnd.Elements.Element import Element
import pygame
from BackEnd import ImageManagement


class Image(Element):
    loaded_url = []
    loaded_image = []
    @staticmethod
    def getLoadedImage(url):
        if url in Image.loaded_url:
            index = Image.loaded_url.index(url)
            print('[Image Management]Fetched loaded image '+url+'.')
            return Image.loaded_image[index]
        else:
            return None
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
            surface = Image.getLoadedImage(self.url)
            if surface != None:
                self.surface = pygame.transform.smoothscale(surface, self.size)
                self.ready = True
                return
            surface = ImageManagement.getLocalImage('./images/'+self.url)
            if surface != None:
                self.surface = pygame.transform.smoothscale(surface, self.size)
                self.ready = True
                print('[Image Management]Fetched stored image '+self.url+'.')
                Image.loaded_url.append(self.url)
                Image.loaded_image.append(surface)
                return
            #Not local
            if self.called == False:
                ImageManagement.downloadImage(self.url)
                self.called = True
                print('[Image Management]Start fetching remote image '+self.url+'.')
            else:
                #called and not returned
                pass
            
    def display(self):
        return self.surface

    def change(self, url):
        self.url = url
        self.ready = False
