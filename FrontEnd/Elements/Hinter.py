from Common.base import *
from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.text_default import text_default
class Hinter(Element):
    font = pygame.font.SysFont('simhei', 70)
    def __init__(self,process,text):
        Element.__init__(self, process)
        self.surface = self.font.render(text,True,(234,102,152))
        self.size = self.surface.get_size()
        windowSize = self.process.window.size
        self.location = ((windowSize[0]-self.size[0])/2 , (windowSize[1]-self.size[1])/2)
    def update(self):
        self.counter += 1
        if self.counter<=51:
            alpha = 5*self.counter
            self.surface.set_alpha(alpha)
            return
        if self.counter<=102:
            return
        alpha = 255-5*(self.counter-102)
        if alpha<0:
            self.destory()
        else:
            self.surface.set_alpha(alpha)

    def destory(self):
        self.process.window.childs.remove(self)
        self.childs.clear()
        del self
def createHinter(process,text):
    try:
        process.window.createChild(Hinter,text)
    except:
        print('[Hinter Error]Cannot creater hinter in process {}.'.format(process))