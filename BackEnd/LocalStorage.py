import shelve
import datetime
import os
import json

PATH = 'C:/Users/dell/Desktop/Codes/FaceLook/'


class LocalStorage(object):
    def __init__(self, username=None, rootPath=None):
        # self.username = username
        # self.rootPath = rootPath
        self.messageRecords = {}
        self.sessionTable = {}
        self.groupList = {}
        self.friendTable = {}
        # new = False
        # if not os.path.exists(self.rootPath + "userdata"):
        #     os.mkdir(self.rootPath + "userdata")
        # if not os.path.exists(self.rootPath + "userdata/" + username):
        #     os.mkdir(self.rootPath + "userdata/" + self.username)
        #     new = True
        # self.messageRecords = shelve.open(self.rootPath + "userdata/" + username + "/messageRecords", writeback=True)
        # self.sessionTable = shelve.open(self.rootPath + "userdata/" + username + "/sessionTable", writeback=True)
        # self.groupList = shelve.open(self.rootPath + "userdata/" + username + "/groupList", writeback=True)
        # self.friendTable = shelve.open(self.rootPath + "userdata/" + username + "/friendTable", writeback=True)
        # if new:
        self.sessionTable['num_of_session'] = 0
        self.groupList['num'] = 0
        self.groupList['list'] = []
        self.friendTable['num'] = 0

    # def openLocal(self):
    #     self.messageRecords = shelve.open(self.rootPath + "userdata/" + self.username + "/messageRecords",
    #                                       writeback=True)
    #     self.sessionTable = shelve.open(self.rootPath + "userdata/" + self.username + "/sessionTable", writeback=True)
    #     self.groupList = shelve.open(self.rootPath + "userdata/" + self.username + "/groupList", writeback=True)
    #     self.friendTable = shelve.open(self.rootPath + "userdata/" + self.username + "/friendTable", writeback=True)

    # def closeLocal(self):
    #     self.messageRecords.close()
    #     self.sessionTable.close()
    #     self.groupList.close()
    #     self.friendTable.close()

    def getSessionByID(self, sessionID):
        # 在存储中获取某会话，若不存在，则创建
        tableItem = self.sessionTable.get(sessionID, None)
        if tableItem is None:
            self.messageRecords[sessionID] = []
            self.sessionTable['num_of_session'] = self.sessionTable.get('num_of_session', 0) + 1
            self.sessionTable[sessionID] = {
                'num_of_message': 0,
                'sessionName': None,
                'managerUsername': None,
                'sessionMembers': [],
                'last_time': None,
                'last_message': None
            }
            tableItem = self.sessionTable.get(sessionID, None)
        return tableItem

    def addGroupList(self, sessionID, sessionName):
        # 添加群聊进入列表
        if self.groupList.get(sessionID, None) is None:
            self.groupList[sessionID] = sessionName
            self.groupList['list'].append(sessionID)
            self.groupList['num'] = self.groupList.get('num', 0) + 1

    def delGroupList(self, sessionID):
        # 删除群聊
        if self.groupList.get(sessionID, None) is not None:
            self.groupList.pop(sessionID)
            self.groupList['list'].remove(sessionID)
            self.groupList['num'] = self.groupList['num'] - 1

    def setFriendForeignKey(self, sessionID, username):
        # 添加username-sessionID键值对
        if self.friendTable.get(username, None) is None:
            self.friendTable['num'] = self.friendTable.get('num', 0) + 1
            self.friendTable[username] = sessionID

    def delFriendForeignKey(self, username):
        if self.friendTable.get(username, None) is not None:
            self.friendTable['num'] = self.friendTable['num'] - 1
            self.friendTable.pop(username)

    def setSessionInfo(self, sessionID, sessionName, managerUsername, sessionMembers):
        tableItem = self.sessionTable.get(sessionID, None)
        if tableItem is not None:
            tableItem['sessionName'] = sessionName
            tableItem['managerUsername'] = managerUsername
            tableItem['sessionMembers'] = sessionMembers

    def addRecordsDict(self, sessionID, records, username=None, sessionName=None, managerUsername=None, sessionMembers=[]):
        # 向存储中添加消息
        # 参数records可为dict或list(dict)
        # 参数username若不为none，则为私聊
        if sessionID is None or records is None:
            return
        try:
            if type(sessionID) is int:
                sessionID = str(sessionID)
            tableItem = self.sessionTable.get(sessionID, None)
            if tableItem is None:
                if username is None:
                    self.addGroupList(sessionID,sessionName)
                elif username is not None:
                    self.setFriendForeignKey(sessionID, username)
                self.messageRecords[sessionID] = []
                self.sessionTable['num_of_session'] = self.sessionTable.get('num_of_session', 0) + 1
                self.sessionTable[sessionID] = {
                    'num_of_message': 0,
                    'sessionName': sessionName,
                    'managerUsername': managerUsername,
                    'sessionMembers': sessionMembers,
                    'last_time': None,
                    'last_message': None
                }
                tableItem = self.sessionTable.get(sessionID, None)
            if type(records) == dict:
                self.messageRecords[sessionID].append(records)
                addNum = {'num_of_message': tableItem['num_of_message'] + 1}
                tableItem.update(addNum)
                tableItem['last_time'] = records.get('time', None)
                tableItem['last_message'] = records
            elif type(records) == list:
                for record in records:
                    self.messageRecords[sessionID].append(record)
                addNum = {'num_of_message': tableItem['num_of_message'] + len(records)}
                tableItem.update(addNum)
                if len(records) > 0:
                    tableItem['last_time'] = records[len(records) - 1].get('time', None)
                    tableItem['last_message'] = records[len(records) - 1]
        except Exception:
            print("error in local storage")

    def rewriteRecord(self, sessionID, records, username=None, sessionName=None, managerUsername=None, sessionMembers=[]):
        # 用records覆盖某会话的存储
        # records为list
        if sessionID is None or records is None:
            return
        try:
            if type(sessionID) is int:
                sessionID = str(sessionID)
            tableItem = self.sessionTable.get(sessionID, None)
            if tableItem == None:
                if username is None:
                    self.addGroupList(sessionID)
                else:
                    self.setFriendForeignKey(sessionID, username)
                self.sessionTable['num_of_session'] = self.sessionTable.get('num_of_session', 0) + 1
            self.messageRecords[sessionID] = []
            self.sessionTable[sessionID] = {
                'num_of_message': 0,
                'sessionName': sessionName,
                'managerUsername': managerUsername,
                'sessionMembers': sessionMembers,
                'last_time': None,
                'last_message': None
            }
            tableItem = self.sessionTable.get(sessionID, None)
            for record in records:
                self.messageRecords[sessionID].append(record)
            addNum = {'num_of_message': tableItem['num_of_message'] + len(records)}
            tableItem.update(addNum)
            if len(records) > 0:
                tableItem['last_time'] = records[len(records) - 1].get('time', None)
                tableItem['last_message'] = records[len(records) - 1]
        except Exception:
            print("error in local storage")

    def getSessionNum(self):
        # 获取该用户本地存储中的会话个数
        return self.sessionTable.get('num_of_session', 0)

    def getMessageNum(self, sessionID):
        if sessionID is not None:
            tableItem = self.sessionTable.get(sessionID, None)
            if tableItem is not None:
                return tableItem.get('num_of_message', 0)
        return 0

    def getRecordNum(self, sessionID):
        # 获取该用户本地存储中，某会话的消息条数
        if sessionID is not None:
            tableItem = self.sessionTable.get(sessionID, None)
            if tableItem == None:
                return 0
            else:
                return tableItem.get('num_of_message', 0)
        else:
            return None

    def getRecords(self, sessionID, num=10):
        # 获取该用户本地存储中，某会话的后num条消息
        # 若没有消息，则返回空list
        if sessionID is None:
            recordList = self.messageRecords.get(sessionID, None)
            numOfMessage = self.getRecordNum(sessionID)
            result = []
            if num > numOfMessage:
                num = numOfMessage
            if recordList != None:
                for i in range(len(recordList) - num, len(recordList)):
                    result.append(recordList[i])
            return result
        else:
            return  None

    def getGroups(self):
        result = []
        grouplist = self.groupList.get('list', None)
        if grouplist is not None:
            for ID in grouplist:
                group = {}
                group['sessionId'] = ID
                group['sessionName'] = self.groupList.get(ID, None)
                group['latestMessage'] = self.getSessionLastMessage(ID)
                result.append(group)
        return result

    # 以下四个函数，若没有消息，则返回None
    def getSessionLastTime(self, sessionID):
        # 获取该用户本地存储中，某会话最后消息的时间
        # 若没有消息，则返回None
        if sessionID is not None:
            tableItem = self.sessionTable.get(sessionID, None)
            if tableItem == None:
                return None
            else:
                return tableItem.get('last_time')
        else:
            return None

    def getSessionLastMessage(self, sessionID):
        # 获取该用户本地存储中，某会话的最后消息
        # 若没有消息，则返回None
        if sessionID is not None:
            tableItem = self.sessionTable.get(sessionID, None)
            if tableItem == None:
                return None
            else:
                return tableItem.get('last_message')
        else:
            return None

    def getFriendLastTime(self, username):
        if username is not None:
            friendSession = self.friendTable.get(username, None)
            if friendSession is None:
                return None
            else:
                return self.get_session_last_time(friendSession)
        else:
            return None

    def getFriendLastMessage(self, username):
        if username is not None:
            friendSession = self.friendTable.get(username, None)
            if friendSession is None:
                return None
            else:
                return self.get_session_last_message(friendSession)
        else:
            return None

    def getSessionContent(self, sessionID):
        if sessionID is not None:
            result = None
            tableItem = self.sessionTable.get(sessionID, None)
            if tableItem is not None:
                result = {}
                result['num_of_message'] = tableItem['num_of_message']
                result['sessionName'] = tableItem['sessionName']
                result['managerUsername'] = tableItem['managerUsername']
                result['sessionMembers'] = tableItem['sessionMembers']
                result['last_time'] = tableItem['last_time']
                result['last_message'] = tableItem['last_message']
                result['contents'] = self.messageRecords.get(sessionID)
            return result
        else:
            return None

    def getFriendSession(self, username):
        if username is not None:
            return self.friendTable.get(username, None)
        else:
            return None

    def getContentByFriend(self, username):
        if username is not None:
            sessionId = self.getFriendSession(username)
            if sessionId is not None:
                return self.getSessionContent(sessionId)
        else:
            return None

    def test(self):
        pass
        # self.setFriendForeignKey("3", "arealdd")
        # self.setFriendForeignKey('4', 'dd')

        # self.messageRecords[self.username] = [[datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '消息1']]
        # self.messageRecords[self.username] += [[datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '消息2']]

        # record1 = {'from':'5477','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'content':'hello'}
        # self.addRecordsDict("1",record1,None,sessionName="name",managerUsername="manager",sessionMembers=['user1','user2'])
        # record3 = {'from':'5477','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'content':'hello'}
        # self.addRecordsDict("3",record3,None)
        # record2 = {'from':'8145','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'content':'nice'}
        # self.addRecordsDict("2",record2,'8145')
        # print(self.getGroups())
        # print(self.getSessionContent("1"))
        # print(self.getContentByFriend("8145"))
        # print(self.getGroups())
        # record4 = {'from':'5477','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'content':'hello'}
        # record5 = {'from':'8145','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'content':'nice'}
        # records = []
        # records.append(record4)
        # records.append(record5)
        # self.rewriteRecord("1",records,None,sessionName="name",managerUsername="manager",sessionMembers=['user1','user2'])
        # print(self.getGroups())
        # print(self.getSessionContent("1"))
        # print(self.getFriendSession(None))
        # print(self.getFriendLastTime("8147"))


# ls = LocalStorage()
# ls.test()