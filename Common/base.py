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


def UserMessage(sender, time, content, kind):
    return {'sender':sender,'time':time,'content':content,'kind':kind}


def Session(sessionID,userMessages):
    return {'sessionID':sessionID,'userMessages':userMessages}


def User(username, password, nickname, avatarURL):
    return {
        'username':username,
        'password':password,
        'nickname':nickname,
        'avatarAddress':avatarURL,
        }


'''def User(username, password, nickname, email, phone, address, avatarURL, enable_invite):
    return {
        'username': username,
        'password': password,
        'nickname': nickname,
        'avatarURL': avatarURL,
        'email': email,
        'phone': phone,
        'address': address,
        'enable_invite': enable_invite,
    }


def Friend(username, nickname, email, phone, address, avatarURL):
    return {
        'nickname': nickname,
        'avatarURL': avatarURL,
        'username': username,
        'email': email,
        'phone': phone,
        'address': address,
    }'''



def ReceiverMessage(receiverUsername, avatarAddress, result, time):
    return {
        'receiverUsername':receiverUsername,
        'avatarAddress':avatarAddress,
        'result':result,
        'time':time,
        }

def RequestorMessage(requestorUsername, avatarAddress, checkMessage, time):
    return {
        'requestorUsername':requestorUsername,
        'avatarAddress':avatarAddress,
        'checkMessage':checkMessage,
        'time':time,
        }
