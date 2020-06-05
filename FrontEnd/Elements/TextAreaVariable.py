from FrontEnd.Elements.Element import Element
import pygame
class TextAreaVariable(Element):
    # 在原本基础上可以调整宽度、左右空白比例、背景图片样式、字体、字号
    text_height_top_rate = 0.1
    text_height_buttom_rate = 0.1
    text_height_rate = 1 - (text_height_top_rate + text_height_buttom_rate)
    
    line_spacing = 10
    def __init__(self,process,location,width,borderRate,imageURL,fonttype,fontsize,text,color):
        Element.__init__(self,process)
        self.font = pygame.font.SysFont(fonttype,fontsize)
        if imageURL == 'white':
            tempBG = pygame.Surface((width,1))
            tempBG.fill((255,255,255))
            self.bubble = tempBG
        else:
            self.bubble = pygame.image.load(imageURL)
        self.bubble_width = width
        self.text_width_left_rate = borderRate
        self.text_width_right_rate = borderRate
        self.text_width_rate = 1 - 2*borderRate
        self.text_width = self.bubble_width * self.text_width_rate
        self.location = location
        self.surface = None
        self.color = color
        self.setText(text)
        
    def alignCenter(self,pos):
        x = pos[0]
        y = pos[1]
        rect = self.surface.get_rect()
        rectX = rect[2]
        rectY = rect[3]
        self.location = (x-rectX//2,y-rectY//2)

    def setText(self,text):
        lines = []
        sentence = ''
        text_height = 0
        line_height = 0
        for char in text:
            sentence_size = self.font.size(sentence+char)
            if line_height<sentence_size[1]:
                line_height = sentence_size[1]
            if sentence_size[0]>self.text_width or char=='\n':
                lines.append(sentence)
                print(sentence_size[0],sentence)
                text_height += sentence_size[1] + self.line_spacing
                if char == '\n':
                    sentence = ''
                else:
                    sentence = char
            else:
                sentence += char
        if sentence:
            lines.append(sentence)
            text_height += sentence_size[1]
            sentence = ''
        bubble_width = int(self.bubble_width)
        bubble_height = int(text_height/self.text_height_rate)
        print('Debug:bubble ',bubble_width,bubble_height)
        self.surface = pygame.transform.smoothscale(self.bubble,(bubble_width,bubble_height))
        drawX = self.text_width_left_rate*bubble_width
        drawY = self.text_height_top_rate*bubble_height
        for line in lines:
            if line == '':
                line = ' '
            self.surface.blit(self.font.render(line,True,self.color),(drawX,drawY))
            drawY += self.line_spacing + line_height