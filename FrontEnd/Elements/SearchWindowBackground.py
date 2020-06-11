from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.SearchPeople import SearchPeople
from FrontEnd.Elements.DropDownMenu import DropDownMenu
from FrontEnd.Elements.SingleInputBox import InputBox
from FrontEnd.Elements.TextButton import TextButton
from FrontEnd.Elements.AddCheckMessage import AddCheckMessage
from FrontEnd.Elements.Button import UserCloseButton, UserMinimizeButton
import pygame


class SearchWindowBackground(Element):
    input_border = pygame.image.load('./resources/SearchWindowUI/people_input_border.png')
    title = pygame.image.load('./resources/SearchWindowUI/title.png')

    def __init__(self, process):
        Element.__init__(self, process)
        self.surface = pygame.Surface((800, 450))
        self.surface.fill((255, 255, 255))
        self.location = (0, 0)
        self.search_people = self.createChild(SearchPeople, (0, 60+40))
        self.check_message = self.createChild(AddCheckMessage, (150, 80+40))
        self.search_people.check = self.check_message
        self.menu = self.createChild(DropDownMenu, (50, 20+40), ['用户名', '昵称'])
        self.input = self.createChild(InputBox, (200, 22+40), 450, 'dengxian', 24, (0, 0, 0), (255, 255, 255))
        self.search_button = self.createChild(SearchButton, (680, 20+40), '搜索', 20, (80, 30))
        self.closeButton = self.createChild(UserCloseButton, (765, 8))
        self.minimizeButton = self.createChild(UserMinimizeButton, (730, 8))

    def getEvent(self, event):
        for child in self.childs:
            if child.active:
                child.getEvent(event)

    def update(self):
        if self.search_button.pressed and self.input.get_text() != '':
            key = self.menu.get_selected()
            self.search_people.childs.clear()
            if key == '昵称':
                request = {
                    'messageNumber': '20',
                    'keyword': self.input.get_text()
                }
                self.process.requestQueue.put(request)
            else:
                request = {
                    'messageNumber': '21',
                    'keyword': self.input.get_text()
                }
                self.process.requestQueue.put(request)
        self.search_button.pressed = False
        for child in self.childs:
            if child.active:
                child.update()

    def display(self):
        surface = self.surface.copy()
        surface.blit(SearchWindowBackground.input_border, (195, 20+40))
        surface.blit(SearchWindowBackground.title, (0, 0))
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        return surface


class SearchButton(TextButton):

    def __init__(self, process, location, text, fontsize, size):
        TextButton.__init__(self, process, location, text, fontsize, size)
        self.pressed = False

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
                self.pressed = True
