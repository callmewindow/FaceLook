from FrontEnd.Elements.Element import Element
import pygame


class TripleStateButton(Element):
    # 0 == idle
    # 1 == hover
    # 2 == select
    image = pygame.Surface((100, 100))
    image_hover = pygame.Surface((100, 100))
    image_select = pygame.Surface((100, 100))
    image.fill((255, 255, 255))
    image_hover.fill((245, 245, 245))
    image_select.fill((235, 235, 235))

    def __init__(self, process, location, image, size):
        Element.__init__(self, process)
        self.size = size
        self.iconsize = (int(size[1] * 0.8), int(size[1] * 0.8))
        self.icon = pygame.transform.smoothscale(pygame.image.load(image), self.iconsize)
        self.image = pygame.transform.smoothscale(self.image, size)
        self.image_hover = pygame.transform.smoothscale(self.image_hover, size)
        self.image_select = pygame.transform.smoothscale(self.image_select, size)
        self.location = location
        self.state = 0

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] <= x <= self.location[0] + self.size[0] \
                and self.location[1] <= y <= self.location[1] + self.size[1]:
            return True
        return False

    def getEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.state != 2:
                if self.pos_in(event.pos):
                    self.state = 1
                else:
                    self.state = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pos_in(event.pos) and event.button == pygame.BUTTON_LEFT:
                if self.state != 2:
                    self.state = 2
                else:
                    self.state = 1
            else:
                self.state = 0

    def display(self):
        if self.state == 0:
            self.surface = self.image
        elif self.state == 1:
            self.surface = self.image_hover
        else:
            self.surface = self.image_select
        surface = self.surface.copy()
        surface.blit(self.icon, ((self.size[0] - self.iconsize[0]) / 2, (self.size[1] - self.iconsize[1]) / 2))
        return surface
