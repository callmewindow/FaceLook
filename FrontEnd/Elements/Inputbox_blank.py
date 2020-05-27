from FrontEnd.Elements.Inputbox import Inputbox
import pygame


class Inputbox_blank(Inputbox):
    image = pygame.transform.smoothscale(pygame.image.load('./resources/inputbox_blank.png'), (290, 40))
    font = pygame.font.SysFont('dengxian', 24)

    def __init__(self, process, location):
        Inputbox.__init__(self, process, location, Inputbox_blank.image, Inputbox_blank.font, (10, 7))
        pygame.key.set_text_input_rect(pygame.Rect(0, 0, 0, 0))

    def posin(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] <= x <= self.location[0] + 300 and self.location[1] <= y <= self.location[1] + 50:
            return True
        return False
