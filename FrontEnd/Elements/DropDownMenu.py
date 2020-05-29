from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.text_default import text_default
import pygame


class DropDownMenu(Element):
    image = pygame.image.load('./resources/UserWindowUI/transparent_background.png')

    def __init__(self, process, location, selections: list):
        Element.__init__(self, process)
        self.location = location
        self.selections = selections
        self.length = len(selections)
        self.surface = pygame.transform.smoothscale(DropDownMenu.image, (120, self.length * 30 + 30))
        self.selected = self.createChild(Selected, (0, 0))
        self.selected.set_text(selections[0])
        self.blocks = []
        for i in range(self.length):
            self.blocks.append(self.createChild(Selections, (0, i * 30 + 30), selections[i]))

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def update(self):
        if self.selected.state == 2:
            for block in self.blocks:
                block.enable()
        else:
            for block in self.blocks:
                block.disable()
        for block in self.blocks:
            if block.is_selected:
                self.selected.set_text(block.text.text)
                block.is_selected = False
        for child in self.childs:
            if child.active:
                child.update()

    def get_selected(self):
        return self.selected.text.text


class Selected(Element):
    image_default = pygame.image.load('./resources/UserWindowUI/dropdown_default.png')
    image_hover = pygame.image.load('./resources/UserWindowUI/dropdown_hover.png')
    image_drop = pygame.image.load('./resources/UserWindowUI/dropdown_drop.png')

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.location = location
        self.text = self.createChild(text_default, (0, 0), 'test', (0, 0, 0))
        self.state = 0
        self.has_selected = False
        self.size = (120, 30)

    def pos_in(self, pos):
        x, y = pos[0], pos[1]
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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.pos_in(event.pos):
                if self.state != 2:
                    self.has_selected = False
                    self.state = 2
                else:
                    self.state = 1
            else:
                self.state = 0

    def update(self):
        if self.state == 0:
            self.surface = Selected.image_default
        elif self.state == 1:
            self.surface = Selected.image_hover
        else:
            self.surface = Selected.image_drop

    def set_text(self, text):
        self.text.setText(text)


class Selections(Element):
    image = pygame.Surface((120, 30))
    image.fill((255, 255, 255))
    image_onHover = pygame.Surface((120, 30))
    image_onHover.fill((245, 245, 245))

    def __init__(self, process, location, text):
        Element.__init__(self, process)
        self.disable()
        self.location = location
        self.text = self.createChild(text_default, (0, 0), text, (0, 0, 0))
        self.is_selected = False
        self.size = (120, 30)
        self.surface = Selections.image

    def pos_in(self, pos):
        x, y = pos[0], pos[1]
        if self.location[0] <= x <= self.location[0] + self.size[0] \
                and self.location[1] <= y <= self.location[1] + self.size[1]:
            return True
        return False

    def getEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.pos_in(event.pos):
                self.surface = Selections.image_onHover
            else:
                self.surface = Selections.image
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            if self.pos_in(event.pos):
                self.is_selected = True
                print(self.text.text)
