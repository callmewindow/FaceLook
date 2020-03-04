from FrontEnd.Elements.Element import Element
import pygame
class Inputbox(Element):
    pygame.font.init()
    def __init__(self,process,location,surface,font,textBias):
        Element.__init__(self,process)
        self.text = ''
        self.focused = False
        self.location = location
        self.surface = surface
        self.font = font
        self.changed = False
        self.textSurface = None
        self.textBias = textBias        
    def addChar(self,ch):
        if len(self.text)>=16:
            return
        self.text += ch
        self.changed = True
    def removeChar(self):
        if len(self.text) == 0:
            return        
        self.text = self.text[0:len(self.text)-1]
        self.changed = True
    def update(self):
        if self.focused:
            self.counter += 1
            if self.counter % 60 ==0:
                self.changed = True
        if self.changed:
            self.changed = False
            if self.focused or self.counter%60 == 0:
                if self.counter <=60 and self.focused:                
                    textValue = self.text+'_'
                else:
                    textValue = self.text
            else:
                textValue = self.text
            if self.counter == 120:
                self.counter = 1
            if textValue != '':
                self.textSurface = self.font.render(textValue,True,(128,128,128))
            else:
                self.textSurface = None
        else:
            pass
    def display(self):
        surface = self.surface.copy()
        if self.textSurface!=None:
            surface.blit(self.textSurface,self.textBias)
        return surface
    def posin(self,pos):
        pass
    def getEvent(self,event):
        if event.type == pygame.constants.MOUSEBUTTONDOWN:
            self.changed = True
            if self.posin(event.pos):
                self.focused = True
                self.changed = True
                self.counter = 1
            else:
                self.changed = True
                self.focused = False

            return

        if event.type == pygame.constants.KEYDOWN and self.focused == True:
            if event.key == pygame.constants.K_BACKSPACE:
                self.removeChar()

        if event.type == pygame.constants.TEXTINPUT and self.focused == True:
            self.addChar(event.text)
                
