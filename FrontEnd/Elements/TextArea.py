from FrontEnd.Elements.Element import Element
import pygame
class TextArea(Element):
    font = pygame.font.SysFont('DENGXIAN',20)
    bubble = pygame.image.load('./resources/bubble.png')
    bubble_width = 300
    
    text_width_left_rate = 0.1
    text_width_right_rate = 0.1
    text_width_rate = 1 - (text_width_left_rate + text_width_right_rate)
    text_width = bubble_width * text_width_rate
    
    text_height_top_rate = 0.1
    text_height_buttom_rate = 0.1
    text_height_rate = 1 - (text_height_top_rate + text_height_buttom_rate)
    
    line_spacing = 10
    def __init__(self,process,location,text,color):
        Element.__init__(self,process)
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
            sentence_size = TextArea.font.size(sentence+char)
            if line_height<sentence_size[1]:
                line_height = sentence_size[1]
            if sentence_size[0]>TextArea.text_width or char=='\n':
                lines.append(sentence)
                print(sentence_size[0],sentence)
                text_height += sentence_size[1] + TextArea.line_spacing
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
        bubble_width = int(TextArea.bubble_width)
        bubble_height = int(text_height/TextArea.text_height_rate)
        print('Debug:bubble ',bubble_width,bubble_height)
        self.surface = pygame.transform.smoothscale(TextArea.bubble,(bubble_width,bubble_height))
        drawX = TextArea.text_width_left_rate*bubble_width
        drawY = TextArea.text_height_top_rate*bubble_height
        for line in lines:
            self.surface.blit(TextArea.font.render(line,True,self.color),(drawX,drawY))
            drawY += TextArea.line_spacing + line_height
            
              
        
    