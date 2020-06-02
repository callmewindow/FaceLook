from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.UserInforWindowBackground import UserInforWindowBackground
class UserInforWindow(Window):
    def __init__(self,process):
        Window.__init__(self,process,'信息查看',(400,500),(63, 115, 163))
        self.bg = self.createChild(UserInforWindowBackground)