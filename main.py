import pygame

pygame.init()
pygame.font.init()
pygame.key.set_repeat()

from FrontEnd.Processes.UserWindowProcess import UserWindowProcess as UWP
from FrontEnd.Processes.LoginWindowProcess import LoginWindowProcess as LWP
from BackEnd.BackEndThread import BackEndThread
from multiprocessing import Process
from Common.base import *
def test_data(data):
    avatar = "image::DEFAULT_AQUA"
    meaAvatar = "image::DEFUALT_MEA"
    mikoAvatar = "image::DEFAULT_MIKO"
    shionAvatar = "image::DEFAULT_SHION"
    matsuriAvatar = "image::DEFAULT_MATSURI"
    fubukiAvatar = "image::DEFAULT_FUBUKI"
    '''
    avatar = pygame.transform.smoothscale(pygame.image.load('./resources/UserData/MinatoAqua/MinatoAqua.jpg'), (75, 75))
    meaAvatar = pygame.transform.smoothscale(pygame.image.load('./resources/UserData/MinatoAqua/cache/mea.jpg'),
                                             (75, 75))
    mikoAvatar = pygame.transform.smoothscale(pygame.image.load('./resources/UserData/MinatoAqua/cache/miko.jpg'),
                                              (75, 75))
    shionAvatar = pygame.transform.smoothscale(pygame.image.load('./resources/UserData/MinatoAqua/cache/shion.jpg'),
                                               (75, 75))
    maziliAvatar = pygame.transform.smoothscale(pygame.image.load('./resources/UserData/MinatoAqua/cache/mazili.jpg'),
                                                (75, 75))
    xiaohuliAvatar = pygame.transform.smoothscale(
        pygame.image.load('./resources/UserData/MinatoAqua/cache/xiaohuli.jpg'), (75, 75))
    '''
    data.user = User('MinatoAqua', 'MinatoAqua', 'Aqua', avatar, UserStateType.ONLINE)

    mea = User('Mea', 'Mea', '消息列表1', meaAvatar, UserStateType.ONLINE)
    miko = User('Miko', 'Miko', '消息列表2', mikoAvatar, UserStateType.ONLINE)
    shion = User('Shion', 'Shion', '消息列表3', shionAvatar, UserStateType.ONLINE)
    mazili = User('Mazili', 'Mazili', '好友列表1', matsuriAvatar, UserStateType.ONLINE)
    xiaohuli = User('Xiaohuli', 'Xiaohuli', '好友列表2', fubukiAvatar, UserStateType.ONLINE)
    miko2 = User('Miko2', 'Miko2', '好友列表3', mikoAvatar, UserStateType.ONLINE)
    shion2 = User('Shion2', 'Shion2', '群组列表1', shionAvatar, UserStateType.ONLINE)
    mazili2 = User('Mazili2', 'Mazili2', '群组列表2', matsuriAvatar, UserStateType.ONLINE)
    xiaohuli2 = User('Xiaohuli2', 'Xiaohuli2', '群组列表3', fubukiAvatar, UserStateType.ONLINE)

    data.messageList = [mea, miko, shion]
    data.friendList = [mazili, xiaohuli, miko2]
    data.groupList = [shion2, mazili2, xiaohuli2]
    
    testUserMessage1 = UserMessage('Fubuki','2020-5-26 15:13','KONKONKON')
    testUserMessage2 = UserMessage('Fubuki','2020-5-26 15:14','KONKONKON')
    testUserMessage3 = UserMessage('Fubuki','2020-5-26 15:15','KONKONKON')
    testUserMessage4 = UserMessage('Fubuki','2020-5-26 15:16','KONKONKON')
    testUserMessage5 = UserMessage('Fubuki','2020-5-26 15:17','KONKONKON')
    data.sessions = [Session(233,[testUserMessage1,testUserMessage2,testUserMessage3,testUserMessage4,testUserMessage5])]
    print(data)
    print([msg.time for msg in data.getSessionByID(233).userMessages])
if __name__ == '__main__':
    RQ = Queue()
    MQ = Queue()
    data = DataCenter()
    bet = BackEndThread(data, RQ, MQ)
    bet.start()
    
    # login
    '''
    lwp = LWP(data, RQ, MQ, bet)
    # print(bet.messageQueue)
    # print(lwp.messageQueue)
    lwp.run()
    '''
    test_data(data)
    uwp = UWP(data, RQ, MQ, bet)
    uwp.run()
    bet.stop()
