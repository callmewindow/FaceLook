from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.Aqua import Aqua
from FrontEnd.Elements.logo import logo
from FrontEnd.Elements.LoginWindowBackgrond import LoginWindowBackground as lwb
import pygame
class LoginWindow(Window):
    def __init__(self,process):
        Window.__init__(self,process,'Login',(600,450),(255,255,255))

        lwbb = self.createChild(lwb)

    def login(self):
        pass