from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.text_default import text_default
import pygame

class text_variable(text_default):
    def __init__(self, process, location, text, fonttype, fontsize, color):
        text_default.font = pygame.font.SysFont(fonttype, fontsize)
        if text == None:
            tempText = "无"
        else:
            tempText = text
        text_default.__init__(self, process, location, tempText, color)
    