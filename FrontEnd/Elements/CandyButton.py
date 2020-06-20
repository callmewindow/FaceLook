from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Hinter import createHinter
from Common.base import *
class CandyButton(Element):
    source_img = pygame.image.load('./resources/LoginWindowUI/login_button.png')
    image = pygame.transform.smoothscale(source_img,(320,55))
    #bigImage = pygame.transform.smoothscale(source_img,(120,60))
    del source_img
    def __init__(self,process,location):
        Element.__init__(self,process)
        self.surface = self.image        
        self.location = location
        self.state = 0
        self.size = (320,55)
        self.max_alpha = 255
        self.min_alpha = 200
        self.transform_frame = 11
        self.delta_alpha = int((self.max_alpha-self.min_alpha)/self.transform_frame)
    def posin(self,pos):
        x = pos[0]
        y = pos[1]
        if self.location[0]<=x and x<=self.location[0]+self.size[0] and self.location[1]<=y and y<=self.location[1]+self.size[1]:
            return True
        return False
    def update(self):
        if self.state == 1:
            if self.counter<self.transform_frame:
                self.counter = self.counter+1
                alpha = self.max_alpha - self.delta_alpha*self.counter
                self.surface.set_alpha(alpha)
        elif self.state == 0:
            if self.counter>0:
                self.counter = self.counter-1
                alpha = self.max_alpha - self.delta_alpha*self.counter
                self.surface.set_alpha(alpha)
    def getEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.posin(event.pos):
                self.state = 1
            else:
                self.state = 0
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and self.posin(event.pos):
            self.process.addAction(Action(ActionType.LOGIN,None))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT and self.posin(event.pos):
            createHinter(self.process,'一个彩蛋')



            
        