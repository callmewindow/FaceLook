from FrontEnd.Elements.Inputbox import Inputbox
import pygame
class Inputbox_password(Inputbox):
    image = pygame.transform.smoothscale(pygame.image.load('./resources/LoginWindowUI/password_inputbox.png'),(320,55))   
    font = pygame.font.SysFont('simhei',30)
    def __init__(self,process,location):
        Inputbox.__init__(self,process,location,Inputbox_password.image,Inputbox_password.font,(50,15))
        #surface = pygame.Surface((300,50))
        #surface.fill((255,255,255))                
        #Inputbox.__init__(self,process,location,surface,Inputbox_default.font,(0,0))
        #self.surface.set_alpha(150)
    def posin(self,pos):
        x = pos[0]
        y = pos[1]
        if self.location[0]<=x and x<=self.location[0]+300 and self.location[1]<=y and y<=self.location[1]+50:
            return True
        return False
    def update(self):
        if self.focused:
            self.counter += 1
            if self.counter % 60 ==0:
                self.changed = True
        if self.changed:
            self.changed = False
            if self.focused or self.counter%60 == 0:
                if self.counter <=60 and self.focused:                
                    textValue = '*'*len(self.text)+'_'
                else:
                    textValue = '*'*len(self.text)
            else:
                textValue = '*'*len(self.text)
            if self.counter == 120:
                self.counter = 1
            if textValue != '':
                self.textSurface = self.font.render(textValue,True,(0,0,0))
            else:
                self.textSurface = None
        else:
            pass
            