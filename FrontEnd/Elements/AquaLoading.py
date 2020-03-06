from FrontEnd.Elements.Element import Element
import pygame
class AquaLoading(Element):
    images = []
    for _ in range(0,5):
        url = './resources/AquaLoading/aqualoading '+str(_)+'.png'
        img = pygame.image.load(url)
        img = pygame.transform.scale(img,(160,160))
        images.append(img)
    def __init__(self,process,location):
        Element.__init__(self,process)
        self.location = location
        self.surface = AquaLoading.images[0]
    def update(self):
        self.counter = (self.counter+1)%25      
        self.surface = AquaLoading.images[self.counter//5]
        return

