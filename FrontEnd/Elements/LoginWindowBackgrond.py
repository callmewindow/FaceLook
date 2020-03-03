import pygame
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.logo import logo
from FrontEnd.Elements.Aqua import Aqua
class LoginWindowBackground(Element):
    def __init__(self,process):
        Element.__init__(self,process)
        self.location = (0,0)
        self.surface = pygame.transform.scale(pygame.image.load('./resources/bg.jpg'),(600,450))
        aqua = self.createChild(Aqua,(166,150))
        logoo = self.createChild(logo,(100,50))
        print(aqua.process)
        print(logoo.process)
