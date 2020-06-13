from FrontEnd.Elements.Element import Element
import pygame


class SingleClickButton(Element):
    # 0 == idle
    # 1 == hover
    # 2 == select
    image = pygame.Surface((100, 100))
    image_hover = pygame.Surface((100, 100))
    image_select = pygame.Surface((100, 100))
    image.fill((255, 255, 255))
    image_hover.fill((245, 245, 245))
    image_select.fill((235, 235, 235))

    def __init__(self, process, location, size, icon_size, url, func: str):
        Element.__init__(self, process)
        self.size = size
        self.icon_size = icon_size
        self.icon = pygame.transform.smoothscale(pygame.image.load(url), icon_size)
        self.image = pygame.transform.smoothscale(SingleClickButton.image, size)
        self.image_hover = pygame.transform.smoothscale(SingleClickButton.image_hover, size)
        self.image_select = pygame.transform.smoothscale(SingleClickButton.image_select, size)
        if func == 'apply':
            self.icon_notice = pygame.transform.smoothscale(
                pygame.image.load('./resources/UserWindowUI/mail_notice.png'), icon_size)
        self.location = location
        self.state = 0
        self.func = func
        self.pressed = False
        self.notice = False

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] < x < self.location[0] + self.size[0] \
                and self.location[1] < y < self.location[1] + self.size[1]:
            return True
        return False

    def getEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.pos_in(event.pos):
                if self.state != 2:
                    self.state = 1
            else:
                self.state = 0
            return
        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP] and self.pos_in(event.pos):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                self.state = 2
            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                self.state = 0
                if self.pos_in(event.pos):
                    if self.func == 'add':
                        self.process.createSearchWindow()
                    elif self.func == 'create':
                        self.pressed = True
                    elif self.func == 'apply':
                        self.notice = False
                        self.process.createFriendApplyWindow()

    def display(self):
        if self.state == 0:
            self.surface = self.image
        elif self.state == 1:
            self.surface = self.image_hover
        else:
            self.surface = self.image_select
        surface = self.surface.copy()
        surface.blit(self.icon, ((self.size[0] - self.icon_size[0]) // 2, (self.size[1] - self.icon_size[1]) // 2))
        if self.func == 'apply' and self.notice:
            surface.blit(self.icon_notice, ((self.size[0] - self.icon_size[0]) // 2, (self.size[1] - self.icon_size[1]) // 2))
        return surface

    def update(self):
        pass
