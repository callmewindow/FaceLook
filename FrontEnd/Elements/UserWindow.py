from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.UserWindowBackground import UserWindowBackground
class UserWindow(Window):
    def __init__(self,process):
        Window.__init__(self,process,'FaceLook!',(350,700),(255,255,255))
        self.bg = self.createChild(UserWindowBackground)
    def getMessage(self, message):
        self.bg.getMessage(self, message)