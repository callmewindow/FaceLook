import threading
import queue
from multiprocessing.queues import Empty
from time import sleep
from BackEnd.SolverThreads import *
from BackEnd.LocalStorage import *
from Common.dataFunction import *


# from SolverThreads import *
# from LocalStorage import *

def init(rq):
    # 初始化，创建TCP连接
    client = TcpClient()
    client.runTcp(rq)
    return client


class RequestType():
    CLOSE = '0'
    INIT = '1r'
    LOGIN = '2'
    LOGINRET = '2r'
    REGISTER = '3'
    REGISTERRET = '3r'
    GETFRIENDLIST = '4'
    GETFRIENDLISTRET = '4r'
    GETHISTORY = '5'
    GETHISTORYRET = '5r'
    CREATESESSION = '6'
    CREATESESSIONRET = '6r'
    JOINSESSION = '7'
    JOINSESSIONRET = '7r'
    GETFRIENDREGISTER = '8'
    GETFRIENDREGISTERRET = '8r'
    SENDMESSAGE = '9'
    SENDMESSAGERET = '9r'
    FRIENDREGISTER = '10'
    FRIENDREGISTERRET = '10r'
    RECEIVEFRIENDREGISTERRET = '11r'
    RESPONDFRIENDREGISTER = '12'
    RESPONDFRIENDREGISTERRET = '12r'
    GETFRIENDREGISTERRESULT = '13'
    GETFRIENDREGISTERRESULTRET = '13r'
    GETFRIENDREGISTERRESULTRETLIST = '14'
    GETFRIENDREGISTERRESULTRETLISTRET = '14r'
    DELETEFRIEND = '15'
    DELETEFRIENDRET = '15r'
    BEDELETEDFRIENDRET = '16r'  # 被删除好友
    EXITSESSION = '17'
    EXITSESSIONRET = '17r'
    UPDATEPERSONALINFORMATION = '18'
    UPDATEPERSONALINFORMATIONRET = '18r'
    UPDATESESSIONINFORMATION = '19'
    UPDATESESSIONINFORMATIONRET = '19r'
    SEARCHBYNICKNAME = '20'
    SEARCHBYNICKNAMERET = '20r'
    SEARCHBYUSERNAME = '21'
    SEARCHBYUSERNAMERET = '21r'
    KICKOUT = '22'
    KICKOUTRET = '22r'


class MessageType():
    LOGINRET = '2r'
    REGISTERRET = '3r'
    GETFRIENDLISTRET = '4r'
    CREATESESSIONRET = '6r'
    JOINSESSIONRET = '7r'
    GETFRIENDREGISTERRET = '8r'
    SENDMESSAGERET = '9r'
    FRIENDREGISTERRET = '10r'
    RECEIVEFRIENDREGISTERRET = '11r'
    RESPONDFRIENDREGISTERRET = '12r'
    GETFRIENDREGISTERRESULTRET = '13r'
    GETFRIENDREGISTERRESULTRETLISTRET = '14r'
    DELETEFRIENDRET = '15r'
    BEDELETEDFRIENDRET = '16r'
    EXITSESSIONRET = '17r'
    UPDATEPERSONALINFORMATIONRET = '18r'
    UPDATESESSIONINFORMATIONRET = '19r'
    SEARCHBYNICKNAMERET = '20r'
    SEARCHBYUSERNAMERET = '21r'
    KICKOUTRET = '22r'


class BackEndThread(threading.Thread):
    def __init__(self, requestQueue, messageQueue, data):
        threading.Thread.__init__(self)
        self.requestQueue = requestQueue
        self.messageQueue = messageQueue
        self.go = True
        self.client = None
        self.username = None
        self.localStorage = LocalStorage()
        self.task = []
        self.data = data
        self.need_session = False
        self.needed_username = ''

    def run(self):
        self.client = init(self.requestQueue)
        sleep(1)
        print(self.data['write_lock'])
        while self.go:
            request = None
            try:
                request = self.requestQueue.get(block=False)
            except Empty:
                pass
            except Exception as e:
                print(e)
            if request is not None:
                self.handleRequest(request)
            sleep(0.1)

    def handleRequest(self, request):
        messageNumber = request.get('messageNumber', None)

        if messageNumber == RequestType.INIT:
            print("连接已建立")
        # 注销
        # request格式：{"messageNumber": "0"}
        elif messageNumber == RequestType.CLOSE:
            thread = Close(self.client)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        # 登录
        # request格式：{"username": "hcz", "password": "123456", "messageNumber": "2"}
        # message格式：见下方
        elif messageNumber == RequestType.LOGIN:
            thread = Login(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.LOGINRET:
            result = request.get('messageField1', None)
            info = request.get('messageField2', None)
            dataj = request.get('messageField3', None)
            try:
                data = readData(self.data)
                if result != '0':
                    user = json.loads(dataj)
                    self.username = user.get('username', None)
                    data['user']['version'] += 1
                    data['user']['username'] = user.get('username', None)
                    data['user']['nickname'] = user.get('nickname', None)
                    data['user']['avatarAddress'] = user.get('avatarAddress', None)
                    data['user']['invitee'] = user.get('invitee', None)
                    data['user']['phoneNumber'] = user.get('phoneNumber', None)
                    data['user']['email'] = user.get('email', None)
                    data['user']['occupation'] = user.get('occupation', None)
                    data['user']['location'] = user.get('location', None)
                    data['user']['login_result'] = result
                    data['user']['login_information'] = info
                elif result == '0':
                    data['user']['version'] += 1
                    data['user']['login_result'] = result
                    data['user']['login_information'] = info
            except KeyError as e:
                print('key error in 2r:')
                print(e)
            except Exception as o:
                print('other error in 2r:')
                print(o)
            lockData(self.data)
            writeData(self.data, data)
            unlockData(self.data)
            self.requestQueue.put({'messageNumber': '5'})
            sleep(1)
            self.requestQueue.put({'messageNumber': '4'})

        # 注册
        # request格式：{"username": "hcz", "password": "123456", "nickname": "quq", "messageNumber": "3"}
        # message格式：见下方
        elif messageNumber == RequestType.REGISTER:
            thread = Register(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.REGISTERRET:
            result = request.get('messageField1', None)
            info = request.get('messageField2', None),
            dataj = request.get('messageField3', None)
            try:
                data = readData(self.data)
                if result != '0':
                    user = json.loads(dataj)
                    self.username = user.get('username', None)
                    data['user']['version'] += 1
                    data['user']['username'] = user.get('username', None)
                    data['user']['nickname'] = user.get('nickname', None)
                    data['user']['avatarAddress'] = user.get('avatarAddress', None)
                    data['user']['invitee'] = user.get('invitee', None)
                    data['user']['phoneNumber'] = user.get('phoneNumber', None)
                    data['user']['email'] = user.get('email', None)
                    data['user']['occupation'] = user.get('occupation', None)
                    data['user']['location'] = user.get('location', None)
                    data['user']['login_result'] = result
                    data['user']['login_information'] = info
                elif result == '0':
                    data['user']['version'] += 1
                    data['user']['login_result'] = result
                    data['user']['login_information'] = info
            except KeyError as e:
                print('key error in 3r:')
                print(e)
            except Exception as o:
                print('other error in 3r:')
                print(o)
            lockData(self.data)
            writeData(self.data, data)
            unlockData(self.data)

        # 获取好友列表
        # request格式：{"messageNumber": "4"}
        # message格式：num表示好友个数，friendlist为一个dict列表，字段分别为username和nickname
        elif messageNumber == RequestType.GETFRIENDLIST:
            thread = GetFriendList(self.client)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.GETFRIENDLISTRET:
            friendNum = request.get('messageField1', None)
            dataj = request.get('messageField2', None)
            try:
                friendlist = json.loads(dataj)
                result = []
                data = readData(self.data)
                if type(friendlist) == list and friendNum != '0':
                    for friend in friendlist:
                        temp = {
                            'username': friend.get('username', None), 'nickname': friend.get('nickname', None),
                            'invitee': friend.get('invitee', None),
                            'avatarAddress': friend.get('avatarAddress', None),
                            'phoneNumber': friend.get('phoneNumber', None), 'email': friend.get('email', None),
                            'occupation': friend.get('occupation', None), 'location': friend.get('location', None),
                            'sessionId': self.localStorage.getFriendSession(friend.get('username', None)),
                            'latestMessage': self.localStorage.getFriendLastMessage(friend.get('username', None))
                            }
                        result.append(temp)
                data['friendList']['version'] += 1
                data['friendList']['list'] = result
            except KeyError as e:
                print('key error in 4r:')
                print(e)
            except Exception as o:
                print('other error in 4r:')
                print(o)
            lockData(self.data)
            writeData(self.data, data)
            unlockData(self.data)

        # 获取历史消息
        # request格式：{"messageNumber": "5"}
        # 无message
        elif messageNumber == RequestType.GETHISTORY:
            thread = GetHistory(self.client)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.GETHISTORYRET:
            sessionNum = request.get('messageField1', None)
            dataj = request.get('messageField2', None)
            try:
                data = readData(self.data)
                resultlist = []
                sessionlist = json.loads(dataj)
                if type(sessionlist) == list and sessionNum != '0' and self.localStorage is not None:
                    for session in sessionlist:
                        sessionID = session.get('sessionId', None)
                        if sessionID is None:
                            continue
                        sessionName = session.get('sessionName', None)
                        managerName = session.get('managerUsername', None)
                        members = session.get('sessionMembers', None)
                        records = session.get('contents', None)
                        if records is not None:
                            records = json.loads(records)
                        if managerName is None and members is not None:
                            # 私聊
                            for name in members:
                                if name != self.username:
                                    username = name
                        else:
                            username = None
                        #更新本地
                        self.localStorage.rewriteRecord(sessionID, records, username, sessionName, managerName, members)
                        #更新data中的sessionList
                        temp = {
                            'sessionId': sessionID,
                            'numOfMessage': self.localStorage.getMessageNum(sessionID),
                            'sessionName': sessionName,
                            'managerUsername': managerName,
                            'sessionMembers': members,
                            'contents': records
                        }
                        resultlist.append(temp)
                data['groupList']['version'] += 1
                data['groupList']['list'] = self.localStorage.getGroups()
                data['sessionList']['version'] += 1
                data['sessionList']['list'] = resultlist
            except KeyError as e:
                print('key error in 5r:')
                print(e)
            except Exception as o:
                print('other error in 5r:')
                print(o)
            lockData(self.data)
            writeData(self.data, data)
            unlockData(self.data)
        # 建立会话并自动加入
        # request格式：{"messageNumber": "6"}
        # message格式：sessionID若为0则表示建立失败
        elif messageNumber == RequestType.CREATESESSION:
            thread = CreateSession(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.CREATESESSIONRET:
            sessionID = request.get('messageField1', None)
            if self.need_session:
                # 如果need_session，即刚刚通过了一个好友请求，那么把这个好友加入刚申请到的无名session中，发5号请求刷新列表
                self.need_session = False
                self.requestQueue.put({
                        'messageNumber': '7',
                        'username': self.needed_username,
                        'sessionId': sessionID
                    })
                self.requestQueue.put({'messageNumber': '5'})
            else:
                # 否则说明刚申请到的session是群聊，那么只发5号请求刷新列表
                self.requestQueue.put({'messageNumber': '5'})

        # 邀请他人加入会话
        # request格式：{"messageNumber": "7","username":"dsm","sessionId":"2"}   (sessionID也可兼容)
        # message格式：见下方
        elif messageNumber == RequestType.JOINSESSION:
            thread = JoinSession(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.JOINSESSIONRET:
            if request.get('messageField1', None) != '1':
                print("邀请加入失败")

        # 获取好友请求列表
        # request格式：{"messageNumber": "8"}
        # message格式：
        elif messageNumber == RequestType.GETFRIENDREGISTER:
            thread = GetFriendRegister(self.client)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.GETFRIENDREGISTERRET:
            registerNum = request.get('messageField1', None)
            dataj = request.get('messageField2', None)
            try:
                registerlist = json.loads(dataj)
                result = []
                data = readData(self.data)
                if type(registerlist) == list and registerNum != '0':
                    for register in registerlist:
                        time = register.get('time', None)
                        if time is not None:
                            Time = time.split('-', 6)
                            time = Time[0] + "年" + Time[1] + "月" + Time[2] + "日"
                        temp = {'requestorUsername': register.get('requestorUsername', None),
                                'checkMessage': register.get('checkMessage', None),
                                'avatarAddress': register.get('avatarAddress', None),
                                'time': time}
                        result.append(temp)
                data['requestorList']['version'] += 1
                data['requestorList']['list'] = result
            except KeyError as e:
                print('key error in 8r:')
                print(e)
            except Exception as o:
                print('other error in 8r:')
                print(o)
            lockData(self.data)
            writeData(self.data, data)
            unlockData(self.data)

        # 发送/接收消息
        # request使用eg：注意时间格式
        # record = {'from':'hcz','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),'content':'hello dsm'}
        # request = {"messageNumber": "9",'sessionID':'2','message':json.dumps(record)} 
        # message格式：见下方，message为一个dict
        elif messageNumber == RequestType.SENDMESSAGE:
            thread = SendMessage(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.SENDMESSAGERET:
            self.requestQueue.put({'messageNumber': '5'})

        # 添加好友，发送好友申请 {'messageNumber':'10'}
        # request格式:{"toUserName":"lex", "checkMessage":"我是你爸爸"， "messageNumber":"10"}
        # message无
        elif messageNumber == RequestType.FRIENDREGISTER:
            thread = FriendRegister(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)

        # 收到好友申请 {'messageNumber':'11r'}
        # request无
        # message格式：
        elif messageNumber == RequestType.RECEIVEFRIENDREGISTERRET:
            try:
                data = readData(self.data)
                data['requestorMessage']['version'] += 1
            except KeyError as e:
                print('key error in 11r:')
                print(e)
            except Exception as o:
                print('other error in 11r:')
                print(o)
            lockData(self.data)
            writeData(self.data, data)
            unlockData(self.data)

        # 回复好友申请
        # request格式：{"fromUsername":"hololive", "result":1, "messageNumber":"12"}
        # result为0表示拒绝，为1表示接受
        # 无message
        elif messageNumber == RequestType.RESPONDFRIENDREGISTER:
            thread = RespondFriendRegister(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
            # 顺便把result处理一下
            result = request.get('result', None)
            if result == '1':
                self.need_session = True
                self.needed_username = request['requestorUsername']
                self.requestQueue.put({'messageNumber': '4'})

        # 用户接收到添加好友申请结果 {'messageNumber':'13r'}
        # request无
        # message格式如下
        elif messageNumber == RequestType.GETFRIENDREGISTERRESULTRET:
            dataj = request.get('messageField1', None)
            result = json.loads(dataj)
            flag = result.get("result", "0")
            if flag == '1':
                self.requestQueue.put({'messageNumber': '4'})
            try:
                data = readData(self.data)
                data['receiverMessage']['version'] += 1
            except KeyError as e:
                print('key error in 13r:')
                print(e)
            except Exception as o:
                print('other error in 13r:')
                print(o)
            lockData(self.data)
            writeData(self.data, data)
            unlockData(self.data)

        # 获取申请结果列表
        # request格式：{'messageNumber':'14'}
        elif messageNumber == RequestType.GETFRIENDREGISTERRESULTRETLIST:
            thread = GetFriendRegisterResultList(self.client)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.GETFRIENDREGISTERRESULTRETLISTRET:
            registerResultNum = request.get('messageField1', None)
            data = request.get('messageField2', None)
            try:
                registerResultList = json.loads(data)
                result = []
                data = readData(self.data)
                if type(registerResultList) == list and registerResultNum != '0':
                    for registerResult in registerResultList:
                        time = registerResult.get('time', None)
                        if time is not None:
                            Time = time.split('-', 6)
                            time = Time[0] + "年" + Time[1] + "月" + Time[2] + "日"
                        temp = {'receiverUsername': registerResult.get('receiverUsername', None),
                                'avatarAddress': registerResult.get('avatarAddress', None),
                                'result': registerResult.get('result', None),
                                'time': time}
                        result.append(temp)
                data['receiverList']['version'] += 1
                data['receiverList']['list'] = result
            except KeyError as e:
                print('key error in 14r:')
                print(e)
            except Exception as o:
                print('other error in 14r:')
                print(o)
            lockData(self.data)
            writeData(self.data, data)
            unlockData(self.data)

        # 删除好友
        # request格式：{'username': 'hamzy', 'messageNumber':'15'}
        elif messageNumber == RequestType.DELETEFRIEND:
            thread = DeleteFriend(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
            self.requestQueue.put({'messageNumber': '4'})

        # 删除好友回复
        # request格式：{'username': 'hamzy', 'messageNumber':'16r'}
        elif messageNumber == RequestType.BEDELETEDFRIENDRET:
            self.requestQueue.put({'messageNumber': '4'})

        # 退出群聊 {'messageNumber':'17'}
        elif messageNumber == RequestType.EXITSESSION:
            thread = ExitSession(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
            self.process.requestQueue.put({'messageNumber': '5'})
        elif messageNumber == RequestType.EXITSESSIONRET:
            pass

        # 更改个人信息 {'messageNumber':'18'}
        elif messageNumber == RequestType.UPDATEPERSONALINFORMATION:
            thread = UpdatePersonalInformation(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.UPDATEPERSONALINFORMATIONRET:
            dataj = request.get('messageField1', None)
            try:
                user = json.loads(dataj)
                data = readData(self.data)
                data['user']['version'] += 1
                data['user']['nickname'] = user.get('nickname', None)
                data['user']['avatarAddress'] = user.get('avatarAddress', None)
                data['user']['invitee'] = user.get('invitee', None)
                data['user']['phoneNumber'] = user.get('phoneNumber', None)
                data['user']['email'] = user.get('email', None)
                data['user']['occupation'] = user.get('occupation', None)
                data['user']['location'] = user.get('location', None)
            except KeyError as e:
                print('key error in 18r:')
                print(e)
            except Exception as o:
                print('other error in 18r:')
                print(o)
            lockData(self.data)
            writeData(self.data, data)
            unlockData(self.data)

        # 更改群聊信息 {'messageNumber':'19'}
        elif messageNumber == RequestType.UPDATESESSIONINFORMATION:
            thread = UpdateSessionInformation(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
            self.process.requestQueue.put({'messageNumber': '5'})

        elif messageNumber == RequestType.UPDATESESSIONINFORMATIONRET:
            pass

        # 通过nickname搜索 {'messageNumber':'20'}
        # requset
        # message
        elif messageNumber == RequestType.SEARCHBYNICKNAME:
            thread = SearchByNickname(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.SEARCHBYNICKNAMERET:
            resultNum = request.get('messageField1', None)
            dataj = request.get('messageField2', None)
            result = []
            try:
                data = readData(self.data)
                userList = json.loads(dataj)
                if type(userList) == list and resultNum != '0':
                    for userResult in userList:
                        temp = {'username': userResult.get('username', None), 'nickname': userResult.get('nickname', None),
                                'invitee': userResult.get('invitee', None),
                                'avatarAddress': userResult.get('avatarAddress', None),
                                'phoneNumber': userResult.get('phoneNumber', None), 'email': userResult.get('email', None),
                                'occupation': userResult.get('occupation', None),
                                'location': userResult.get('location', None)}
                        result.append(temp)
                data['nicknameResult']['version'] += 1
                data['nicknameResult']['list'] = result
            except KeyError as e:
                print('key error in 20r:')
                print(e)
            except Exception as o:
                print('other error in 20r:')
                print(o)
            lockData(self.data)
            writeData(self.data, data)
            unlockData(self.data)

        # 通过username搜索 {'messageNumber':'21'}
        elif messageNumber == RequestType.SEARCHBYUSERNAME:
            thread = SearchByUsername(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.SEARCHBYUSERNAMERET:
            resultNum = request.get('messageField1', None)
            dataj = request.get('messageField2', None)
            try:
                data = readData(self.data)
                user = {}
                if resultNum != '0':
                    user = json.loads(dataj)
                result = []
                if type(user) == dict and resultNum != '0':
                    temp = {'username': user.get('username', None), 'nickname': user.get('nickname', None),
                            'invitee': user.get('invitee', None), 'avatarAddress': user.get('avatarAddress', None),
                            'phoneNumber': user.get('phoneNumber', None), 'email': user.get('email', None),
                            'occupation': user.get('occupation', None), 'location': user.get('location', None)}
                    result.append(temp)
                data['usernameResult']['version'] += 1
                data['usernameResult']['list'] = result
            except KeyError as e:
                print('key error in 21r:')
                print(e)
            except Exception as o:
                print('other error in 21r:')
                print(o)
            lockData(self.data)
            writeData(self.data, data)
            unlockData(self.data)

        # 群主踢人 {'messageNumber':'22'}
        elif messageNumber == RequestType.KICKOUT:
            thread = KickOut(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
            self.process.requestQueue.put({'messageNumber': '5'})
        elif messageNumber == RequestType.KICKOUTRET:
            pass
        else:
            self.stop()

    def stop(self):
        quitLogin = {"messageNumber": "0"}
        self.requestQueue.put(quitLogin)
        for tk in self.task:
            tk.join(timeout=1)
        if self.client is not None:
            self.client.closeServer()
        else:
            print("尚未建立连接")
        self.go = False

    def requestFailure(self):
        pass
