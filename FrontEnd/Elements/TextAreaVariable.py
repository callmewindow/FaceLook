from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.TextArea import TextArea
import pygame
class TextAreaVariable(TextArea):
    # 在原本基础上可以调整宽度、左右空白比例、背景图片样式、字体、字号
    def __init__(self,process,location,width,borderRate,imageURL,fonttype,fontsize,text,color):
        TextArea.font = pygame.font.SysFont(fonttype,fontsize)
        if imageURL == 'white':
            tempBG = pygame.Surface((width,1))
            tempBG.fill((255,255,255))
            TextArea.bubble = tempBG
        else:
            TextArea.bubble = pygame.image.load(imageURL)
        TextArea.bubble_width = width
        TextArea.text_width_left_rate = borderRate
        TextArea.text_width_right_rate = borderRate
        TextArea.text_width_rate = 1 - 2*borderRate
        TextArea.text_width = TextArea.bubble_width * TextArea.text_width_rate
        TextArea.__init__(self,process,location,text,color)