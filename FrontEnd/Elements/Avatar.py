from FrontEnd.Elements.Element import Element
import pygame
from cv2 import VideoCapture,imshow
class Avatar(Element):
    def __init__(self,process,location):
        Element.__init__(self,process)
        self.location = location
        self.surface = pygame.Surface((100,100))
    def update(self):
        pass