import pygame
from FrontEnd.Elements.Element import Element
import win32gui
import win32con
import win32api
import windnd
class Window(Element):
    def onDragFiles(self,msg):
        print(msg) #Notice: msg is the files' name in form of BYTES ARRAY, not string.
    def __init__(self,process,caption,size,color):
        Element.__init__(self,process)
        self.color = color
        pygame.display.set_caption(caption)        
        self.FPSClock=pygame.time.Clock()
        self.surface = pygame.display.set_mode(size)
        self.surface.fill(color)
        self.size = size
        self.alpha = 255
        #self.origin = pygame.Surface.copy(self.surface)
        self.hwnd = pygame.display.get_wm_info()['window']
        windnd.hook_dropfiles(self.hwnd,self.onDragFiles)

    def display(self):
        #self.surface.fill(self.color)
        self.update()
        for child in self.childs:
            self.surface.blit(child.display(),child.location)
    def getMessage(self,message):
        pass
    
    def set_alpha(self,alpha):        
        try:
            if alpha<0 or alpha>255:
                return
            exstyle = win32api.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
            if 0 == (exstyle & 0x80000):
                exstyle |= win32con.WS_EX_LAYERED
                win32api.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, exstyle)
            win32gui.SetLayeredWindowAttributes(self.hwnd, 0, alpha, win32con.LWA_ALPHA)
            
        except:
            print('[Error]Cannot set window\'s alpha. Are you using Windows OS?')
            return
        self.alpha = alpha
