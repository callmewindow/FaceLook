from FrontEnd.Elements.Element import Element
#from FrontEnd.Elements.Aqua import Aqua
from FrontEnd.Elements.Inputbox_default import Inputbox_default
from FrontEnd.Elements.Inputbox_password import Inputbox_password
from FrontEnd.Elements.CandyButton import CandyButton
from FrontEnd.Elements.text_default import text_default
from FrontEnd.Elements.Button import CloseButton, MinimizeButton
from Common.base import *
from time import sleep
class RegisterUsernameInputbox(Inputbox_default):
    image = pygame.transform.smoothscale(pygame.image.load('./resources/RegisterWindowUI/username_inputbox.png'),(320,61))
class RegisterPasswordInputbox(Inputbox_password):
    image = pygame.transform.smoothscale(pygame.image.load('./resources/RegisterWindowUI/password_inputbox.png'),(320,61))
class RegisterNicknameInputbox(Inputbox_default):
    image = pygame.transform.smoothscale(pygame.image.load('./resources/RegisterWindowUI/nickname_inputbox.png'),(320,61))
class RegisterCandy(CandyButton):
    image = pygame.transform.smoothscale(pygame.image.load('./resources/RegisterWindowUI/register_and_login.png'),(320,55))
    def getEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.posin(event.pos):
                self.state = 1
            else:
                self.state = 0
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and self.posin(event.pos):
            self.process.addAction(Action(ActionType.REGISTER,None))

class RegisterWindowBackground(Element):

    def __init__(self, process):
        Element.__init__(self, process)
        self.location = (0, 0)
        self.state = 0
        self.counter = 0
        self.surface = pygame.transform.smoothscale(pygame.image.load('./resources/LoginWindowUI/loginbg.png'), (600, 450))
        # aqua = self.createChild(Aqua,(450,300))
        self.usernameInputbox = self.createChild(RegisterUsernameInputbox, (140, 80),(90,15))
        self.passwordInputbox = self.createChild(RegisterPasswordInputbox, (140, 170),(90,15))
        self.nicknameInputbox = self.createChild(RegisterNicknameInputbox, (140, 260),(90,15))
        #self.usernameInputbox = self.createChild(InputBox,(150,175),300,'simhei',30,(0,0,0),(255,255,255))
        #self.passwordInputbox = self.createChild(InputBox,(150,250),300,'simhei',30,(0,0,0),(255,255,255))
        self.candy = self.createChild(RegisterCandy, (140, 350))

        self.closeButton = self.createChild(CloseButton, (600 - 40, 4))
        self.minimizeButton = self.createChild(MinimizeButton, (600 - 40 * 2, 4))

    def update(self):
        Element.update(self)
