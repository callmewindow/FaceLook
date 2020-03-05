from sys import exit
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
    def __init__(self,type,content):
        self.type = type
        self.content = content
class Message():
    def __init__(self,type,content):
        self.type = type
        self.content = content
class Request():
    def __init__(self,type,content):
        self.type = type
        self.content = content
class UserMessage():
    def __init__(self,sessionID,content):
        self.sessionID = sessionID
        self.content = content
class Session():
    def __init__(self,sessionID,userMessages):
        self.sessionID = sessionID
        self.userMessages = userMessages
class User():
    def __init__(self,username,password,nickname,avatar,state):
        self.username = username
        self.password = password
        self.nickname = nickname
        self.avatar = avatar
        self.state = state
class Friend():
    def __init__(self,nickname,avatar,state):
        self.nickname = nickname
        self.avatar = avatar
        self.state = state
class FriendList():
    def __init__(self,friendList):
        self.friendList = friendList
class DataCenter():
    def __init__(self):
        self.user = None
        self.friendList = None
        self.sessions = None
        
    
