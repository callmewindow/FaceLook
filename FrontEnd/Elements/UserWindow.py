from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.UserWindowBackground import UserWindowBackground
from Common.base import readData, writeData


class UserWindow(Window):
    def __init__(self, process):
        Window.__init__(self, process, 'FaceLook!', (350, 740), (255, 255, 255), True)
        self.bg = self.createChild(UserWindowBackground)
        self.set_rounded_rectangle(20)

    '''def getMessage(self, message):

        data = readData(self.data)
        try:
            if message['messageNumber'] == '2r':
                data['user'] = message['user']
            writeData(self.data, data)
        except KeyError:
            print('key error in message')
        self.bg.getMessage(self, message)'''
