import threading 
import queue
from multiprocessing.queues import Empty
from time import sleep
from BackEnd.SolverThreads import *
from BackEnd.LocalStorage import *
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
    BEDELETEDFRIENDRET = '16r'#被删除好友
    EXITSESSION = '17'
    UPDATEPERSONALINFORMATION = '18'
    UPDATEPERSONALINFORMATIONRET = '18r'
    UPDATESESSIONINFORMATION = '19'
    UPDATESESSIONINFORMATIONRET = '19r'
    SEARCHBYNICKNAME = '20'
    SEARCHBYNICKNAMERET = '20r'
    SEARCHBYUSERNAME = '21'
    SEARCHBYUSERNAMERET = '21r'


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
    UPDATEPERSONALINFORMATIONRET = '18r'
    UPDATESESSIONINFORMATIONRET = '19r'
    SEARCHBYNICKNAMERET = '20r'
    SEARCHBYUSERNAMERET = '21r'


class BackEndThread(threading.Thread):
    def __init__(self, requestQueue, messageQueue):
        threading.Thread.__init__(self)
        self.requestQueue = requestQueue
        self.messageQueue = messageQueue
        self.threadList = list()
        self.go = True
        self.client = None
        self.username = None
        self.localStorage = None
        self.task = []

    def run(self):
        self.client = init(self.requestQueue)
        sleep(1)

        while self.go:
            request = None
            try:
                request = self.requestQueue.get(block=False)
                #print('this request:',request)
            except Empty:
                pass
            except Exception as e:
                print(e)
            if request is not None:
                self.handleRequest(request)
            sleep(0.1)

    def handleRequest(self, request):
        messageNumber = request.get('messageNumber',None)
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
            data = request.get('messageField3', None)
            user = {}
            if result != '0':
                user = json.loads(data)
                self.username = user.get('username', None)
            message = {
                'messageNumber': MessageType.LOGINRET,
                'result': result,
                'information': request.get('messageField2', None),
                'username': user.get('username', None),
                'nickname': user.get('nickname', None),
                'avatarAddress': user.get('avatarAddress', None),
                'invitee': user.get('invitee', None),
                'phoneNumber': user.get('phoneNumber', None),
                'email': user.get('email', None),
                'occupation': user.get('occupation', None),
                'location': user.get('location', None)
            }
            self.messageQueue.put(message)
            if result != '0' and self.username != None:
                self.localStorage = LocalStorage(self.username)
        # 注册
        # request格式：{"username": "hcz", "password": "123456", "nickname": "quq", "messageNumber": "3"}
        # message格式：见下方
        elif messageNumber == RequestType.REGISTER:
            thread = Register(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.REGISTERRET:
            result = request.get('messageField1',None)
            data = request.get('messageField3', None)
            user = {}
            if result != '0':
                user = json.loads(data)
                self.username = user.get('username', None)
            message = {
                'messageNumber': MessageType.REGISTERRET,
                'result': request.get('messageField1',None),
                'information': request.get('messageField2',None),
                'username': user.get('username', None),
                'nickname': user.get('nickname', None),
                'invitee': user.get('invitee', None),
                'avatarAddress': user.get('avatarAddress', None),
                'phoneNumber': user.get('phoneNumber', None),
                'email': user.get('email', None),
                'occupation': user.get('occupation', None),
                'location': user.get('location', None)
            }
            self.messageQueue.put(message)
            if result != '0' and self.username != None:
                self.localStorage = LocalStorage(self.username)
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
            data = request.get('messageField2', None)
            friendlist = json.loads(data)
            result = []
            if type(friendlist) == list and friendNum != '0':
                for friend in friendlist:
                    temp = {'username': friend.get('username', None), 'nickname': friend.get('nickname', None),
                            'invitee': friend.get('invitee', None), 'avatarAddress': friend.get('avatarAddress', None),
                            'phoneNumber': friend.get('phoneNumber', None), 'email': friend.get('email', None),
                            'occupation': friend.get('occupation', None), 'location': friend.get('location', None)}
                    result.append(temp)
            message = {
                'messageNumber': MessageType.GETFRIENDLISTRET,
                'num': friendNum,
                'friendlist': result
            }
            self.messageQueue.put(message)
        # 获取历史消息
        # request格式：{"messageNumber": "5"}
        # 无message
        elif messageNumber == RequestType.GETHISTORY:
            thread = GetHistory(self.client)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.GETHISTORYRET:
            sessionNum = request.get('messageField1',None)
            data = request.get('messageField2',None)
            sessionlist = json.loads(data)
            if type(sessionlist)== list and sessionNum != '0' and self.localStorage is not None:
                for session in sessionlist:
                    sessinID = session.get('sessionId',None)
                    if sessinID is None:
                        continue
                    sessionName = session.get('sessionName',None)
                    managerName = session.get('managerUsername',None)
                    members = session.get('sessionMembers',None)
                    records = session.get('contents',None)
                    if records is not None:
                        records = json.loads(records)
                    if managerName is None and members is not None:
                        #私聊
                        for name in members:
                            if name != self.username:
                                username = name
                    else:
                        username = None
                    self.localStorage.rewriteRecord(sessinID,records,username,sessionName,managerName,members)
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
            message = {
                'messageNumber': MessageType.CREATESESSIONRET,
                'sessionId': sessionID
            }
            self.messageQueue.put(message)
            # if sessionID != 0 and self.localStorage is not None:
            #     self.localStorage.addSession(sessionID)
        # 邀请他人加入会话
        # request格式：{"messageNumber": "7","username":"dsm","sessionId":"2"}   (sessionID也可兼容)
        # message格式：见下方
        elif messageNumber == RequestType.JOINSESSION:
            thread = JoinSession(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.JOINSESSIONRET:
            message = {
                'messageNumber': MessageType.JOINSESSIONRET,
                'result': request.get('messageField1', None)
            }
            self.messageQueue.put(message)
        # 获取好友请求列表
        # request格式：{"messageNumber": "8"}
        # message格式：
        elif messageNumber == RequestType.GETFRIENDREGISTER:
            thread = GetFriendRegister(self.client)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.GETFRIENDREGISTERRET:
            registerNum = request.get('messageField1',None)
            data = request.get('messageField2',None)
            registerlist = json.loads(data)
            result = []
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
            message = {
                'messageNumber':MessageType.GETFRIENDREGISTERRET,
                'requestorNum': registerNum,
                'requestorList': result
            }
            self.messageQueue.put(message)

        #发送/接收消息
        # request使用eg：注意时间格式
        # record = {'from':'hcz','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),'content':'hello dsm'}
        # request = {"messageNumber": "9",'sessionID':'2','message':json.dumps(record)} 
        # message格式：见下方，message为一个dict
        elif messageNumber == RequestType.SENDMESSAGE:
            thread = SendMessage(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
            sessionID = request.get('messageField1', None)
            if sessionID is None:
                sessionID = request.get('sessionId', None)
                if sessionID is None:
                    sessionID = request.get('sessionID')
            message = request.get('messageField2', None)
            if message is None:
                message = request.get('content', None)
            if message is not None:
                if type(message) is not dict:
                    content = json.loads(message)
                else:
                    content = message
            if self.localStorage is not None:
                self.localStorage.addRecordsDict(sessionID, content)

        elif messageNumber == RequestType.SENDMESSAGERET:
            data = request.get('messageField2', None)
            if data is not None:
                content = json.loads(data)
            sessionID = request.get('messageField1', None)
            username = request.get('messageField3',None)
            message = {
                'messageNumber': MessageType.SENDMESSAGERET,
                'sessionId': sessionID,
                'content': content
            }
            self.messageQueue.put(message)
            if self.localStorage is not None:
                self.localStorage.addRecordsDict(sessionID, content, username)

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
            Request = request.get('messageField1', None)
            print(Request)
            dictRequest = {}
            if Request is not None:
                dictRequest = json.loads(Request)
            time = dictRequest.get('time', None)
            if time is not None:
                Time = time.split('-', 6)
                time = Time[0] + "年" + Time[1] + "月" + Time[2] + "日"
            message = {
                'messageNumber': MessageType.RECEIVEFRIENDREGISTERRET,
                'requestorUsername': dictRequest.get('requestorUsername', None),
                'avatarAddress': dictRequest.get('avatarAddress', None),
                'checkMessage': dictRequest.get('checkMessage', None),
                'time': time
            }
            self.messageQueue.put(message)

        # 回复好友申请
        # request格式：{"fromUsername":"hololive", "result":1, "messageNumber":"12"}
        # result为0表示拒绝，为1表示接受
        # 无message
        elif messageNumber == RequestType.RESPONDFRIENDREGISTER:
            thread = RespondFriendRegister(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
            # 顺便把result还给前端
            message = {
                'messageNumber': MessageType.RESPONDFRIENDREGISTERRET,
                'result': request.get('result', None)
            }
            self.messageQueue.put(message)
        # 用户接收到添加好友申请结果 {'messageNumber':'13r'}
        # request无
        # message格式如下
        elif messageNumber == RequestType.GETFRIENDREGISTERRESULTRET:
            Result = request.get('messageField1', None)
            dictResult = {}
            if Result is not None:
                dictResult = json.loads(Result)
            time = dictResult.get('time', None)
            if time is not None:
                Time = time.split('-', 6)
                time = Time[0] + "年" + Time[1] + "月" + Time[2] + "日"
            message = {
                'messageNumber': MessageType.GETFRIENDREGISTERRESULTRET,
                'receiverUsername': dictResult.get('receiverUsername', None),
                'avatarAddress': dictResult.get('avatarAddress', None),
                'result': dictResult.get('result', None),
                'time': time
            }
            self.messageQueue.put(message)

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
            registerResultList = json.loads(data)
            result = []
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
            message = {
                'messageNumber': MessageType.GETFRIENDREGISTERRESULTRETLISTRET,
                'receiverNum': registerResultNum,
                'receiverList': result
            }
            self.messageQueue.put(message)

        # 删除好友
        # request格式：{'username': 'hamzy', 'messageNumber':'15'}
        elif messageNumber == RequestType.DELETEFRIEND:
            thread = DeleteFriend(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
            # 顺便把消息给前端发回去
            message = {
                'messageNumber': MessageType.DELETEFRIENDRET,
                'username': request.get('username', None)
            }
            self.messageQueue.put(message)
        # 删除好友回复
        # request格式：{'username': 'hamzy', 'messageNumber':'16r'}
        elif messageNumber == RequestType.BEDELETEDFRIENDRET:
            friendNum = request.get('messageField1', None)
            data = request.get('messageField2', None)
            friendlist = json.loads(data)
            result = []
            if type(friendlist) == list and friendNum != '0':
                for friend in friendlist:
                    temp = {'username': friend.get('username', None), 'nickname': friend.get('nickname', None),
                            'invitee': friend.get('invitee', None), 'avatarAddress': friend.get('avatarAddress', None),
                            'phoneNumber': friend.get('phoneNumber', None), 'email': friend.get('email', None),
                            'occupation': friend.get('occupation', None), 'location': friend.get('location', None)}
                    result.append(temp)
            message = {
                'messageNumber': MessageType.BEDELETEDFRIENDRET,
                'num': friendNum,
                'friendlist': result
            }
            self.messageQueue.put(message)
        # 退出群聊 {'messageNumber':'17'}
        elif messageNumber == RequestType.EXITSESSION:
            thread = ExitSession(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        # 更改个人信息 {'messageNumber':'18'}
        elif messageNumber == RequestType.UPDATEPERSONALINFORMATION:
            thread = UpdatePersonalInformation(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.UPDATEPERSONALINFORMATIONRET:
            data = request.get('messageField1', None)
            user = json.loads(data)
            message = {
                'messageNumber': MessageType.UPDATEPERSONALINFORMATIONRET,
                'username': None,
                'password': None,
                'nickname': user.get('nickname', None),
                'avatarAddress': user.get('avatarAddress', None),
                'invitee': user.get('invitee', None),
                'phoneNumber': user.get('phoneNumber', None),
                'email': user.get('email', None),
                'occupation': user.get('occupation', None),
                'location': user.get('location', None)
            }
            self.messageQueue.put(message)
        # 更改群聊信息 {'messageNumber':'19'}
        elif messageNumber == RequestType.UPDATESESSIONINFORMATION:
            thread = UpdateSessionInformation(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
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
            data = request.get('messageField2', None)
            userList = json.loads(data)
            # print(userList)
            result = []
            if type(userList) == list and resultNum != '0':
                for userResult in userList:
                    temp = {'username': userResult.get('username', None), 'nickname': userResult.get('nickname', None),
                            'invitee': userResult.get('invitee', None), 'avatarAddress': userResult.get('avatarAddress', None),
                            'phoneNumber': userResult.get('phoneNumber', None), 'email': userResult.get('email', None),
                            'occupation': userResult.get('occupation', None), 'location': userResult.get('location', None)}
                    result.append(temp)
            message = {
                'messageNumber': MessageType.SEARCHBYNICKNAMERET,
                'num': resultNum,
                'userlist': result
            }
            self.messageQueue.put(message)
        # 通过username搜索 {'messageNumber':'21'}
        elif messageNumber == RequestType.SEARCHBYUSERNAME:
            thread = SearchByUsername(self.client, request)
            thread.setDaemon(True)
            thread.start()
            self.task.append(thread)
        elif messageNumber == RequestType.SEARCHBYUSERNAMERET:
            resultNum = request.get('messageField1', None)
            data = request.get('messageField2', None)
            user = {}
            if resultNum != '0':
                user = json.loads(data)
            result = []
            if type(user) == dict and resultNum != '0':
                temp = {'username': user.get('username', None), 'nickname': user.get('nickname', None),
                        'invitee': user.get('invitee', None), 'avatarAddress': user.get('avatarAddress', None),
                        'phoneNumber': user.get('phoneNumber', None), 'email': user.get('email', None),
                        'occupation': user.get('occupation', None), 'location': user.get('location', None)}
                result.append(temp)
            message = {
                'messageNumber': MessageType.SEARCHBYUSERNAMERET,
                'num': resultNum,
                'userlist': result
            }
            self.messageQueue.put(message)
        else:
            self.stop()
        
    def stop(self):
        quitLogin = {"messageNumber": "0"}
        self.requestQueue.put(quitLogin)
        for tk in self.task:
            tk.join(timeout = 1)
        if self.client is not None:
            self.client.closeServer()
        else:
            print("尚未建立连接")
        self.go = False
        if self.localStorage != None:
            self.localStorage.close()

    def requestFailure(self):
        pass