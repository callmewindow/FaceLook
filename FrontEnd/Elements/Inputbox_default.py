from FrontEnd.Elements.Inputbox import Inputbox
from Common.base import *
class Inputbox_default(Inputbox):
    image = pygame.transform.smoothscale(pygame.image.load('./resources/LoginWindowUI/username_inputbox.png'),(320,55))   
    font = pygame.font.SysFont('simhei',30)
    def __init__(self,process,location,text_bias=(50,13)):
        Inputbox.__init__(self,process,location,self.image,self.font,text_bias)
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
            