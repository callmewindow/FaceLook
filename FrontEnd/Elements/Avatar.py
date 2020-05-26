from FrontEnd.Elements.Element import Element
import pygame


class Avatar(Element):
    avatarBorder = pygame.image.load('./resources/avatarborder.png')

    def __init__(self, process, location, url):
        Element.__init__(self, process)
        self.location = location
        self.url = url
        self.surface = pygame.surface((75,75))
        self.surface.fill((50,100,150))
        self.border = Avatar.avatarBorder

    def display(self):
        surface = pygame.Surface.copy(self.surface)
        surface.blit(self.border, (0, 0))
        surface.set_colorkey((1, 1, 1))
        return surface

    def update(self):
        pass
