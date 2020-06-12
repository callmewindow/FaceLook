from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.AlertWindowBackground import AlertWindowBackground
import pygame
from Common.base import *
import sys

class AlertWindow(Window):
    def __init__(self,process):
        Window.__init__(self,process,'警告窗口',(350,200),(255,255,255),True)
        self.bg = self.createChild(AlertWindowBackground)
        self.set_rounded_rectangle(10)