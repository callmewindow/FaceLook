from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.logo import logo
#from FrontEnd.Elements.Aqua import Aqua
from FrontEnd.Elements.Inputbox_default import Inputbox_default
from FrontEnd.Elements.Inputbox_password import Inputbox_password
from FrontEnd.Elements.TripleStateButton import TripleStateButton
from FrontEnd.Elements.CandyButton import CandyButton
from FrontEnd.Elements.AquaLoading import AquaLoading
from FrontEnd.Elements.text_default import text_default
from FrontEnd.Elements.Button import CloseButton, MinimizeButton
from FrontEnd.Elements.SingleInputBox import InputBox
from Common.base import *
from time import sleep


class login_state():
    login = 0
    loading = 1
    success = 2
    failure = 3


class LoginWindowBackground(Element):

    def __init__(self, process):
        Element.__init__(self, process)
        self.location = (0, 0)
        self.state = 0
        self.counter = 0
        self.surface = pygame.transform.smoothscale(pygame.image.load('./resources/LoginWindowUI/loginbg.png'), (600, 450))
        # aqua = self.createChild(Aqua,(450,300))
        self.logo = self.createChild(logo, (84, 50))
        self.usernameInputbox = self.createChild(Inputbox_default, (140, 175))
        self.passwordInputbox = self.createChild(Inputbox_password, (140, 260))
        #self.usernameInputbox = self.createChild(InputBox,(150,175),300,'simhei',30,(0,0,0),(255,255,255))
        #self.passwordInputbox = self.createChild(InputBox,(150,250),300,'simhei',30,(0,0,0),(255,255,255))
        self.candy = self.createChild(CandyButton, (140, 345))
        self.aqualoading = self.createChild(AquaLoading, (230, 145))
        self.loadingText = self.createChild(text_default, (263, 325), '登录中...', (0, 0, 0))
        self.loadingText.alignCenter((300, 350))
        self.messageText = self.createChild(text_default, (0, 0), '登录失败！', (0, 0, 0))
        self.messageText.alignCenter((300, 332))
        self.aqualoading.disable()
        self.loadingText.disable()
        self.messageText.disable()

        self.closeButton = self.createChild(CloseButton, (600 - 40, 4))
        self.minimizeButton = self.createChild(MinimizeButton, (600 - 40 * 2, 4))

    def set_loading(self):
        self.state = 1
        self.counter = 0
        self.logo.disable()
        self.usernameInputbox.disable()
        self.passwordInputbox.disable()
        self.candy.disable()
        self.messageText.disable()
        self.aqualoading.enable()
        self.loadingText.enable()

    def set_success(self):
        self.state = 2
        self.counter = 0
        self.loadingText.setText('登录成功！正在加载资源...')
        sleep(1)
        self.process.stop()

    def set_failure(self, failureMessage):
        self.state = 3
        self.counter = 0
        self.logo.enable()
        self.usernameInputbox.enable()
        self.passwordInputbox.enable()
        self.candy.enable()
        self.messageText.enable()
        self.aqualoading.disable()
        self.loadingText.disable()
        self.messageText.setText(failureMessage)
    '''
    def getMessage(self, message):
        result = message.get('result', None)
        info = message.get('information', None)
        print(result, info)
        if self.state == login_state.loading:
            if result == '1':
                self.set_success()
                data = readData(self.process.data)
                try:
                    if message['messageNumber'] == '2r':
                        data['user'] = {
                            'username': message['username'],
                            'nickname': message['nickname'],
                            'avatarAddress': message['avatarAddress'],
                            'invitee': message['invitee'],
                            'phoneNumber': message['phoneNumber'],
                            'email': message['email'],
                            'occupation': message['occupation'],
                            'location': message['location'],
                        }
                except KeyError:
                    print('key error in 2r')
                writeData(self.process.data, data)
                self.process.requestQueue.put({'messageNumber': '5'})
                self.process.requestQueue.put({'messageNumber': '4'})
                sleep(1)
                self.process.stop()
            elif result == '0':
                self.set_failure(info)
            return
        print('[Warning]Message', message, 'abandoned.')
    '''
    
    def update(self):
        if self.state == login_state.loading:
            self.counter += 1
            loading_time = self.counter // 60
            self.loadingText.setText('登录中...耗时{}秒'.format(loading_time))
            self.loadingText.alignCenter((300, 350))
            if self.counter%60 == 0:
                if readData(self.process.data).get('user') == None:
                    panic('[Fatal Error]data has no attribute user.')
                login_result = readData(self.process.data)['user'].get('login_result')
                if login_result == '1':
                    self.set_success()
                elif login_result == '0':
                    failureMessage = readData(self.process.data)['user'].get('login_infomation')
                    if failureMessage == None:
                        failureMessage = '未知错误。'
                    self.set_failure(failureMessage)
                elif login_result == '-1':
                    if loading_time >= 30:
                        self.set_failure('登录超时！请检查网络状况。')
                else:
                    panic('[Fatal Error]Unknown data.user.login_result value {}.'.format(login_result))
                
                
        Element.update(self)
