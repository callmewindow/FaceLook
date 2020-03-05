import pygame
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.logo import logo
from FrontEnd.Elements.Aqua import Aqua
from FrontEnd.Elements.Inputbox_default import Inputbox_default
from FrontEnd.Elements.Inputbox_password import Inputbox_password
from FrontEnd.Elements.CandyButton import CandyButton
class LoginWindowBackground(Element):
    '''
    images = []
    for _ in range(0,8):
        url = './resources/Train/train {}.png'.format(str(_))
        img = pygame.transform.scale(pygame.image.load(url),(600,450))
        images.append(img)
    '''
    def __init__(self,process):
        Element.__init__(self,process)
        self.location = (0,0)
        self.surface = pygame.transform.scale(pygame.image.load('./resources/bg.png'),(800,450))
        #aqua = self.createChild(Aqua,(450,300))
        self.logo = self.createChild(logo,(100,50))
        self.usernameInputbox = self.createChild(Inputbox_default,(150,175))
        self.passwordInputbox = self.createChild(Inputbox_password,(150,250))
        candy = self.createChild(CandyButton,(250,350))
    def update(self):
        for child in self.childs:
            child.update()
        
