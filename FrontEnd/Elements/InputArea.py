from FrontEnd.Elements.Element import Element
from typing import Tuple
import pygame


class InputArea(Element):
    cursor_image = pygame.image.load('./resources/input_cursor.png')

    # 位置，宽高，字体，字号，字色，背景色。高度最好是(字号*1.05后向上取整)的整数倍
    def __init__(self, process, location, size: Tuple[int, int], font_type: str, font_size: int,
                 font_color: Tuple[int, int, int], background_color: Tuple[int, int, int]):
        Element.__init__(self, process)
        self.text = ''
        self.text_group = ['']
        self.focused = False
        self.changed = False
        self.location = location
        self.font = pygame.font.SysFont(font_type, font_size)
        self.font_color = font_color
        self.size = size
        self.line_height = self.font.size('a')[1]+4
        self.cursor_index = 0
        self.cursor_pos = (0, 0)
        self.cursor_count = 0
        self.cursor_image = pygame.transform.smoothscale(InputArea.cursor_image, (1, self.line_height))
        self.index = 0
        self.max_line = size[1] // self.line_height
        self.surface = pygame.Surface(size)
        self.surface.fill(background_color)

    def add_char(self, ch):
        self.text = self.text[0:self.cursor_index] + ch + self.text[self.cursor_index:]
        self.cursor_index += len(ch)
        self.changed = True

    def backspace_char(self):
        if len(self.text) == 0 or self.cursor_index == 0:
            return
        self.text = self.text[0:self.cursor_index - 1] + self.text[self.cursor_index:]
        self.cursor_index -= 1
        self.changed = True

    def delete_char(self):
        if len(self.text) == self.cursor_index:
            return
        self.text = self.text[0:self.cursor_index] + self.text[self.cursor_index + 1:]
        self.changed = True

    def new_line(self):
        self.text = self.text[0:self.cursor_index] + '\n' + self.text[self.cursor_index:]
        self.cursor_index += 1
        self.changed = True

    def update(self):
        if self.changed:
            self.changed = False
            self.cursor_count = 0
            i = 0
            self.text_group = ['']
            if self.cursor_index == 0:
                self.cursor_pos = (0, 0)
            for ch in self.text:
                i += 1
                if ch == '\n':
                    self.text_group.append('')
                    if i == self.cursor_index:
                        self.cursor_pos = (len(self.text_group) - 1, 0)
                elif self.font.size(self.text_group[-1] + ch)[0] > self.size[0]:
                    self.text_group.append(ch)
                    if i == self.cursor_index:
                        self.cursor_pos = (len(self.text_group) - 1, 1)
                else:
                    self.text_group[-1] += ch
                    if i == self.cursor_index:
                        self.cursor_pos = (len(self.text_group) - 1, len(self.text_group[-1]))
            if self.cursor_pos[0] < self.index:
                self.index = self.cursor_pos[0]
            elif self.cursor_pos[0] + 1 > self.index + self.max_line:
                self.index = self.cursor_pos[0] - self.max_line + 1
        self.cursor_count = (self.cursor_count + 1) if self.cursor_count < 60 else 0

    def display(self):
        surface = self.surface.copy()
        for i in range(len(self.text_group)):
            if self.text_group[i] != '':
                surface.blit(self.font.render(self.text_group[i], True, self.font_color),
                             (0, (i - self.index) * self.line_height))
            if self.focused and i == self.cursor_pos[0] and self.cursor_count < 30:
                surface.blit(self.cursor_image, (
                    self.font.size(self.text_group[i][0:self.cursor_pos[1]])[0], (i - self.index) * self.line_height))
        return surface

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if self.pos_in(event.pos):
                    if not self.focused:
                        self.changed = True
                    self.focused = True
                else:
                    self.focused = False
                return
            if event.button == pygame.BUTTON_WHEELDOWN and self.index + self.max_line < len(self.text_group):
                self.index += 1
                return
            if event.button == pygame.BUTTON_WHEELUP and self.index > 0:
                self.index -= 1
                return
        if event.type == pygame.KEYDOWN and self.focused:
            if event.key == pygame.K_BACKSPACE:
                self.backspace_char()
            if event.key == pygame.K_DELETE:
                self.delete_char()
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.new_line()
            if event.key == pygame.K_LEFT and self.cursor_index > 0:
                self.cursor_index -= 1
                self.changed = True
            if event.key == pygame.K_RIGHT and self.cursor_index < len(self.text):
                self.cursor_index += 1
                self.changed = True
        if event.type == pygame.TEXTINPUT and self.focused:
            self.add_char(event.text)

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] <= x <= self.location[0] + self.size[0] \
                and self.location[1] <= y <= self.location[1] + self.size[1]:
            return True
        return False

    def getContent(self):
        tempString = "\n".join(self.text_group)
        return tempString