from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.SearchWindowBackground import SearchWindowBackground


class SearchWindow(Window):
    def __init__(self, process):
        Window.__init__(self, process, '添加好友', (800, 450), (255, 255, 255), True)
        self.set_rounded_rectangle(20)
        self.bg = self.createChild(SearchWindowBackground)
