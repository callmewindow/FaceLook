from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.UserWindowBackground import UserWindowBackground
class UserWindow(Window):
    def __init__(self,process):
        Window.__init__(self,process,'FaceLook!',(350,740),(255,255,255),True)
        self.bg = self.createChild(UserWindowBackground)
        self.set_rounded_rectangle(20)
    def getMessage(self, message):
        self.bg.getMessage(self, message)