import pygame
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.logo import logo
from FrontEnd.Elements.Aqua import Aqua
from FrontEnd.Elements.Inputbox_default import Inputbox_default
from FrontEnd.Elements.Inputbox_password import Inputbox_password
from FrontEnd.Elements.CandyButton import CandyButton
from FrontEnd.Elements.AquaLoading import AquaLoading
from FrontEnd.Elements.text_default import text_default
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
        self.surface = pygame.transform.smoothscale(pygame.image.load('./resources/bg.png'),(800,450))
        #aqua = self.createChild(Aqua,(450,300))
        self.logo = self.createChild(logo,(100,50))
        self.usernameInputbox = self.createChild(Inputbox_default,(150,175))
        self.passwordInputbox = self.createChild(Inputbox_password,(150,250))
        self.candy = self.createChild(CandyButton,(250,350))
        self.aqualoading = self.createChild(AquaLoading,(230,145))
        self.loadingText = self.createChild(text_default,(263,325),'登录中...',(0,0,0))
        self.loadingText.alignCenter((300,350))
        self.aqualoading.disable()
        self.loadingText.disable()
    def set_loading(self):
        self.state = 1
        self.logo.disable()
        self.usernameInputbox.disable()
        self.passwordInputbox.disable()
        self.candy.disable()
        self.aqualoading.enable()
        self.loadingText.enable()
    def set_success(self):
        print(self.loadingText.location)
        self.loadingText.setText('登录成功！正在加载资源...')
        print(self.loadingText.location)
        
        
        
        
