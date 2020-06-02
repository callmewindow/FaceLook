from sys import exit
from queue import Queue



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
    def __init__(self, sender, time, content):
        self.sender = sender
        self.time = time
        self.content = content


class Session():
    def __init__(self, sessionID, userMessages):
        self.sessionID = sessionID
        self.userMessages = userMessages


class User():
    def __init__(self, username, password, nickname, avatarURL, state):
        self.username = username
        self.password = password
        self.nickname = nickname
        self.avatarURL = avatarURL
        self.state = state

    def get_username(self):
        return self.username

    def get_nickname(self):
        return self.nickname

    def get_avatarURL(self):
        return self.avatarURL

class Friend():
    def __init__(self, nickname, avatarURL, state):
        self.nickname = nickname
        self.avatarURL = avatarURL
        self.state = state


class FriendList():
    def __init__(self, friendList):
        self.friendList = friendList


class DataCenter():
    def __init__(self):
        self.user = User(None,None,None,None,None)
        self.friendList = []
        self.groupList = []
        self.messageList = []
        self.sessions = None
    def getUser(self):
        return self.user
    def setUser(self, user):
        self.user = user
    def getFriendList(self):
        return self.friendList
    def setFriendList(self,friendList):
        self.friendList = friendList
    def getGroupList(self):
        return self.groupList
    def setGroupList(self,groupList):
        self.groupList = groupList
    def getMessageList(self):
        return self.messageList
    def setMessageList(self,messageList):
        self.messageList = messageList
    def setSessions(self,ses):
        self.sessions = ses
    def getSessions(self):
        print(6)
        return self.sessions
    def getSessionByID(self,sid):
        print(len(self.sessions))
        for session in self.sessions:
            if session.sessionID == sid:
                return session
        return None



