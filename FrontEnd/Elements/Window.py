from Common.base import *
from FrontEnd.Elements.Element import Element
class Window(Element):
    def __init__(self,process,caption,size,color,noframe=False):
        Element.__init__(self,process)
        self.color = color
        pygame.display.set_caption(caption)        
        self.FPSClock=pygame.time.Clock()
        self.noframe = noframe
        if self.noframe:
            self.surface = pygame.display.set_mode(size,pygame.NOFRAME)
        else:
            self.surface = pygame.display.set_mode(size)
        self.surface.fill(color)
        self.size = size
        self.alpha = 255
        #self.origin = pygame.Surface.copy(self.surface)
        self.hwnd = pygame.display.get_wm_info()['window']
        
    def setDragFilesCallback(self,func):

        windnd.hook_dropfiles(self.hwnd,func)

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
    def set_location(self,location):

        win32gui.SetWindowPos(self.hwnd,win32con.HWND_TOPMOST,location[0],location[1],self.size[0],self.size[1],win32con.SWP_SHOWWINDOW)
    def minimize(self):
        pygame.display.iconify()
    def set_rounded_rectangle(self,pixel):

        wr = win32gui.GetWindowRect(self.hwnd)
        PyGdiHANDLE = win32gui.CreateRoundRectRgn(0,0,wr[2]-wr[0],wr[3]-wr[1],pixel,pixel)
        win32gui.SetWindowRgn(self.hwnd,PyGdiHANDLE,False) 
