from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.Aqua import Aqua
class LoginWindow(Window):
    def __init__(self,process):
        Window.__init__(self,'Login',(600,450),(255,255,255),process)
        self.createChild(Aqua,(0,0))