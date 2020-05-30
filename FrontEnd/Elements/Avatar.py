from FrontEnd.Elements.Element import Element
import pygame


class Avatar(Element):
    avatarBorder = pygame.image.load('./resources/avatarborder.png')

    def __init__(self, process, location, url):
        Element.__init__(self, process)
        self.location = location
        self.url = url
        if url == 'image::DEFAULT_AQUA':
            self.surface = pygame.transform.smoothscale(pygame.image.load('./resources/UserData/MinatoAqua/MinatoAqua.jpg'), (75, 75))
        if url == 'image::DEFUALT_MEA':
            self.surface = pygame.transform.smoothscale(pygame.image.load('./resources/UserData/MinatoAqua/cache/mea.jpg'), (75, 75))
        if url == 'image::DEFAULT_MIKO':
            self.surface = pygame.transform.smoothscale(pygame.image.load('./resources/UserData/MinatoAqua/cache/miko.jpg'), (75, 75))
        if url == 'image::DEFAULT_SHION':
            self.surface = pygame.transform.smoothscale(pygame.image.load('./resources/UserData/MinatoAqua/cache/shion.jpg'), (75, 75))
        if url == 'image::DEFAULT_MATSURI':
            self.surface = pygame.transform.smoothscale(pygame.image.load('./resources/UserData/MinatoAqua/cache/mazili.jpg'), (75, 75))
        if url == 'image::DEFAULT_FUBUKI':
            self.surface = pygame.transform.smoothscale(pygame.image.load('./resources/UserData/MinatoAqua/cache/xiaohuli.jpg'), (75, 75))

        '''self.surface = pygame.Surface((75,75))
        self.surface.fill((50,100,150))'''
        self.border = Avatar.avatarBorder

    def display(self):
        surface = pygame.Surface.copy(self.surface)
        surface.blit(self.border, (0, 0))
        surface.set_colorkey((1, 1, 1))
        return surface

    def update(self):
        pass
