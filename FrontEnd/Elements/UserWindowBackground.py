from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Avatar import Avatar
import pygame
class UserWindowBackground(Element):
    image = pygame.transform.scale(pygame.image.load('./resources/userwindowbackground.jpg'),(350,170))
    def __init__(self,process):
        Element.__init__(self,process)
        self.surface = pygame.Surface((350,700))
        self.surface.fill((255,255,255))
        self.surface.blit(UserWindowBackground.image,(0,0))
        self.location = (0,0)
        self.createChild(Avatar,(50,50))
        