from FrontEnd.Elements.Window import Window
class UserWindow(Window):
    def __init__(self,process):
        Window.__init__(self,'Q5',(400,700),(255,255,255),process)