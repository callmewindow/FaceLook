from FrontEnd.Elements.Inputbox import Inputbox
import pygame
class Inputbox_default(Inputbox):
    image = pygame.transform.scale(pygame.image.load('./resources/inputbox.jpg'),(300,50))    
    font = pygame.font.SysFont('dengxian',40)
    def __init__(self,process,location):
        #Inputbox.__init__(self,process,location,Inputbox_default.image,Inputbox_default.font,(0,0))
        surface = pygame.Surface((300,50))
        surface.fill((255,255,255))                
        Inputbox.__init__(self,process,location,surface,Inputbox_default.font,(0,0))
        self.surface.set_alpha(150)
        pygame.key.set_text_input_rect(pygame.Rect(300,300,400,400))
    def posin(self,pos):
        x = pos[0]
        y = pos[1]
        if self.location[0]<=x and x<=self.location[0]+300 and self.location[1]<=y and y<=self.location[1]+50:
            return True
        return False
            