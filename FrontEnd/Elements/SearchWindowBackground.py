from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.SearchPeople import SearchPeople
from FrontEnd.Elements.DropDownMenu import DropDownMenu
from FrontEnd.Elements.SingleInputBox import InputBox
from FrontEnd.Elements.TextButton import TextButton
from FrontEnd.Elements.AddCheckMessage import AddCheckMessage
import pygame


class SearchWindowBackground(Element):
    input_border = pygame.image.load('./resources/SearchWindowUI/people_input_border.png')

    def __init__(self, process):
        Element.__init__(self, process)
        self.surface = pygame.Surface((800, 450))
        self.surface.fill((255, 255, 255))
        self.location = (0, 0)
        self.search_people = self.createChild(SearchPeople, (0, 60))
        self.check_message = self.createChild(AddCheckMessage, (150, 80))
        self.search_people.check = self.check_message
        self.menu = self.createChild(DropDownMenu, (50, 20), ['用户名', '昵称', '手机号', '邮箱', '职业', '地区'])
        self.input = self.createChild(InputBox, (200, 22), 450, 'dengxian', 24, (0, 0, 0), (255, 255, 255))
        self.search_button = self.createChild(SearchButton, (680, 20), '搜索', 20, (80, 30))

    def getEvent(self, event):
        for child in self.childs:
            if child.active:
                child.getEvent(event)

    def update(self):
        if self.search_button.pressed and self.input.get_text() != '':
            key = self.menu.get_selected()
            key = 0 if key == '用户名' else 1 if key == '昵称' else 2 if key == '手机号' else 3 if key == '邮箱' else 4 if key == '职业' else 5
            print(key)
            print(self.input.get_text())
            '''request = {
                'messageNumber': '19',
                'keyword': self.input.get_text(),
                'key': key,
            }
            self.process.requestQueue.put(request)'''
        self.search_button.pressed = False
        for child in self.childs:
            if child.active:
                child.update()

    def display(self):
        surface = self.surface.copy()
        surface.blit(SearchWindowBackground.input_border, (195, 20))
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
            if self.state != 2:
                if self.pos_in(event.pos):
                    self.state = 1
                else:
                    self.state = 0
        if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP) and self.pos_in(event.pos):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                self.state = 2
            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                self.state = 0
                self.pressed = True
