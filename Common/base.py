from sys import exit
from queue import Queue
RQ = Queue()
MQ = Queue()

def panic():
    raise Exception()


class ActionType():
    QUIT = 0
    LOGIN = 1
    REGISTER = 2


class MessageType():
    INIT = 0
    LOGIN = 1
    REGISTER = 2
    GETFRIENDLIST = 3
    SENDUSERMESSAGE = 4


class RequestType():
    INIT = 0
    LOGIN = 1
    REGISTER = 2


class UserStateType():
    OFFLINE = 0
    ONLINE = 1


class Action():
    def __init__(self, type, content):
        self.type = type
        self.content = content


class Message():
    def __init__(self, type, content):
        self.type = type
        self.content = content


class Request():
    def __init__(self, type, content):
        self.type = type
        self.content = content


class UserMessage():
    def __init__(self, sessionID, content):
        self.sessionID = sessionID
        self.content = content


class Session():
    def __init__(self, sessionID, userMessages):
        self.sessionID = sessionID
        self.userMessages = userMessages


class User():
    def __init__(self, username, password, nickname, avatar, state):
        self.username = username
        self.password = password
        self.nickname = nickname
        self.avatar = avatar
        self.state = state


class Friend():
    def __init__(self, nickname, avatar, state):
        self.nickname = nickname
        self.avatar = avatar
        self.state = state


class FriendList():
    def __init__(self, friendList):
        self.friendList = friendList


class DataCenter():
    def __init__(self):
        self.user = None
        self.friendList = None
        self.groupList = None
        self.messageList = None
        self.sessions = None


def FETEXT(data):
    import pygame
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

    data.user = User('MinatoAqua', 'MinatoAqua', 'Aqua', avatar, UserStateType.ONLINE)

    mea = User('Mea', 'Mea', '消息列表1', meaAvatar, UserStateType.ONLINE)
    miko = User('Miko', 'Miko', '消息列表2', mikoAvatar, UserStateType.ONLINE)
    shion = User('Shion', 'Shion', '消息列表3', shionAvatar, UserStateType.ONLINE)
    mazili = User('Mazili', 'Mazili', '好友列表1', maziliAvatar, UserStateType.ONLINE)
    xiaohuli = User('Xiaohuli', 'Xiaohuli', '好友列表2', xiaohuliAvatar, UserStateType.ONLINE)
    miko2 = User('Miko2', 'Miko2', '好友列表3', mikoAvatar, UserStateType.ONLINE)
    shion2 = User('Shion2', 'Shion2', '群组列表1', shionAvatar, UserStateType.ONLINE)
    mazili2 = User('Mazili2', 'Mazili2', '群组列表2', maziliAvatar, UserStateType.ONLINE)
    xiaohuli2 = User('Xiaohuli2', 'Xiaohuli2', '群组列表3', xiaohuliAvatar, UserStateType.ONLINE)

    data.messageList = [mea, miko, shion]
    data.friendList = [mazili, xiaohuli, miko2]
    data.groupList = [shion2, mazili2, xiaohuli2]
