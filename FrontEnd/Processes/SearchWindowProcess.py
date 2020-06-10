import pygame
from FrontEnd.Elements.SearchWindow import SearchWindow
from FrontEnd.Processes.WindowProcess import WindowProcess
from Common.base import *


class SearchWindowProcess(WindowProcess):
    def __init__(self, data, RQ, MQ):
        self.data = data

        WindowProcess.__init__(self, data, RQ, MQ, None, SearchWindow(self))

    def run(self):
        while self.go:
            if self.dragging:
                new_mouse_pos = pyautogui.position()
                if new_mouse_pos[0] != self.mouse_pos[0] or new_mouse_pos[1] != self.mouse_pos[1]:
                    new_window_pos = (self.window_pos[0] + new_mouse_pos[0] - self.mouse_pos[0],
                                      self.window_pos[1] + new_mouse_pos[1] - self.mouse_pos[1])
                    self.window.set_location(new_window_pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    self.go = False
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and not self.dragging and \
                        self.title_rect[0] <= event.pos[0] <= self.title_rect[2] and \
                        self.title_rect[1] <= event.pos[1] <= self.title_rect[3]:
                    self.dragging = True
                    windowRect = win32gui.GetWindowRect(self.hwnd)
                    self.window_pos = (windowRect[0], windowRect[1])
                    self.mouse_pos = pyautogui.position()
                    del windowRect
                if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT and self.dragging:
                    self.dragging = False
                self.window.getEvent(event)
            for action in self.actionList:
                self.doAction(action)
            self.actionList.clear()
            self.window.display()
            pygame.display.update()
            self.window.FPSClock.tick(self.FPS)


def createSearch(data,RQ,MQ):
    swp = SearchWindowProcess(data,RQ,MQ)
    swp.run()
