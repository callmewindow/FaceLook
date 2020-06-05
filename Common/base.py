from sys import exit
import win32gui,win32con,win32api,windnd
import pyautogui
from BackEnd import ImageManagement
def panic():
    raise Exception()
def readData(data):
    return data['inner']
def writeData(data,data_copy):
    data['inner'] = data_copy


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


def UserMessage(sender, time, content):
    return {'sender':sender,'time':time,'content':content}


def Session(sessionID,userMessages):
    return {'sessionID':sessionID,'userMessages':userMessages}


def User(username, password, nickname, avatarURL, state):
    return {
        'username':username,
        'password':password,
        'nickname':nickname,
        'avatarURL':avatarURL,
        'state':state
        }


def Friend(nickname,avatarURL,state):
    return {
        'nickname':nickname,
        'avatarURL':avatarURL,
        'state':state
        }




