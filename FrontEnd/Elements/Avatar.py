from FrontEnd.Elements.Image import Image
import pygame


class Avatar(Image):
    avatarBorder = pygame.image.load('./resources/avatarborder.png')

    def __init__(self, process, location, size, url):
        Image.__init__(self, process, location, size, url)
        self.cover = pygame.transform.smoothscale(Avatar.avatarBorder, size)

    def display(self):
        surface = self.surface.copy()
        surface.blit(self.cover, (0, 0))
        return surface
