import shelve
import datetime
import os
import json

PATH = 'C:/Users/dell/Desktop/Codes/FaceLook/'


class LocalStorage(object):
    def __init__(self, username):
        self.username = username
        self.messageRecords = None
        new = False
        if not os.path.exists(PATH+"userdata/"+username):
            os.mkdir(PATH+"userdata/"+self.username)
            new = True
        self.messageRecords = shelve.open(PATH+"userdata/"+username+"/messageRecords",writeback=True)
        self.sessionTable = shelve.open(PATH+"userdata/"+username+"/sessionTable",writeback=True)
        self.groupList = shelve.open(PATH+"userdata/"+username+"/groupList",writeback=True)
        self.friendTable = shelve.open(PATH+"userdata/"+username+"/friendTable",writeback=True)
        if new:
            self.sessionTable['num_of_session'] = 0
            self.groupList['num'] = 0
            self.groupList['list'] = []
            self.friendTable['num'] = 0


    def getSessionByID(self,sessionID):
        #在存储中获取某会话，若不存在，则创建
        tableItem = self.sessionTable.get(sessionID,None)
        if tableItem == None:
            self.messageRecords[sessionID] = []
            self.sessionTable['num_of_session'] = self.sessionTable.get('num_of_session',0)+1
            self.sessionTable[sessionID] = {
                'num_of_message' : 0,
                'sessionName' : None,
                'managerUsername' : None,
                'sessionMembers' : [],
                'last_time' : None,
                'last_message' : None
            }
            tableItem = self.sessionTable.get(sessionID,None)
        return tableItem

    def addGroupList(self,sessionID):
        #添加群聊
        grouplist = self.groupList.get('list',None)
        if grouplist is not None:
            if self.sessionTable.get(sessionID) is None:
                grouplist.append(sessionID)
        else:
            self.groupList['list'] = []
            self.groupList['list'].append(sessionID)

    def setFriendForeignKey(self,sessionID,username):
        #添加username-sessionID键值对
        tableItem = self.friendTable.get(username,None)
        if tableItem is None:
            self.friendTable['num'] = self.friendTable.get('num',0) + 1
            self.friendTable[username] = sessionID

    def setSessionInfo(self,sessionID,sessionName,managerUsername,sessionMembers):
        tableItem = self.sessionTable.get(sessionID,None)
        if tableItem is not None:
            tableItem['sessionName'] = sessionName
            tableItem['managerUsername'] = managerUsername
            tableItem['sessionMembers'] = sessionMembers

    def addRecordsDict(self,sessionID,records,username=None):
        #向存储中添加消息
        #参数records可为dict或list(dict)
        #参数username若不为none，则为私聊
        if type(sessionID) is int:
            sessionID = str(sessionID)
        tableItem = self.sessionTable.get(sessionID,None)
        if tableItem == None:
            if username is None :
                self.addGroupList(sessionID)
            elif username is not None:
                self.setFriendForeignKey(sessionID,username)
            self.messageRecords[sessionID] = []
            self.sessionTable['num_of_session'] = self.sessionTable.get('num_of_session',0)+1
            self.sessionTable[sessionID] = {
                'num_of_message' : 0,
                'sessionName' : None,
                'managerUsername' : None,
                'sessionMembers' : [],
                'last_time' : None,
                'last_message' : None
            }
            tableItem = self.sessionTable.get(sessionID,None)
        if type(records) == dict:
            self.messageRecords[sessionID].append(records)
            addNum = {'num_of_message':tableItem['num_of_message']+1}
            tableItem.update(addNum)
            tableItem['last_time'] = records.get('time',None)
            tableItem['last_message'] = records
        elif type(records) == list:
            for record in records:
                self.messageRecords[sessionID].append(record)
            addNum = {'num_of_message':tableItem['num_of_message']+len(records)}
            tableItem.update(addNum)
            if len(records) > 0 :
                tableItem['last_time'] = records[len(records)-1].get('time',None)
                tableItem['last_message'] = records[len(records)-1]

    def rewriteRecord(self,sessionID,records,username,sessionName,managerUsername,sessionMembers):
        #用records覆盖某会话的存储
        #records为list
        if type(sessionID) is int:
            sessionID = str(sessionID)
        tableItem = self.sessionTable.get(sessionID,None)
        if tableItem == None:
            if username is None :
                self.addGroupList(sessionID)
            else:
                self.setFriendForeignKey(sessionID,username)
            self.sessionTable['num_of_session'] = self.sessionTable.get('num_of_session',0)+1
        self.messageRecords[sessionID] = []
        self.sessionTable[sessionID] = {
                'num_of_message' : 0,
                'sessionName' : sessionName,
                'managerUsername' : managerUsername,
                'sessionMembers' : sessionMembers,
                'last_time' : None,
                'last_message' : None
            }
        tableItem = self.sessionTable.get(sessionID,None)
        for record in records:
            self.messageRecords[sessionID].append(record)
        addNum = {'num_of_message':tableItem['num_of_message']+len(records)}
        tableItem.update(addNum)
        if len(records) > 0 :
            tableItem['last_time'] = records[len(records)-1].get('time',None)
            tableItem['last_message'] = records[len(records)-1]


    def getSessionNum(self):
        #获取该用户本地存储中的会话个数
        return self.sessionTable.get('num_of_session',0)


    def getRecordNum(self,sessionID):
        #获取该用户本地存储中，某会话的消息条数
        tableItem = self.sessionTable.get(sessionID,None)
        if tableItem == None:
            return 0
        else:
            return tableItem.get('num_of_message',0)


    def getRecords(self,sessionID,num=10):
        #获取该用户本地存储中，某会话的后num条消息
        #若没有消息，则返回空list
        recordList = self.messageRecords.get(sessionID,None)
        numOfMessage = self.getRecordNum(sessionID)
        result = []
        if num > numOfMessage:
            num = numOfMessage
        if recordList != None:
            for i in range(len(recordList)-num,len(recordList)):
                result.append(recordList[i])
        return result

    def getLastTime(self,sessionID):
        #获取该用户本地存储中，某会话最后消息的时间
        #若没有消息，则返回None
        tableItem = self.sessionTable.get(sessionID,None)
        if tableItem == None:
            return None
        else:
            return tableItem.get('last_time')

    def getLastMessage(self,sessionID):
        #获取该用户本地存储中，某会话的最后消息
        #若没有消息，则返回None
        tableItem = self.sessionTable.get(sessionID,None)
        if tableItem == None:
            return None
        else:
            return tableItem.get('last_message')

    def get_groups(self):
        result = []
        grouplist = self.groupList.get('list',None)
        if grouplist is not None:
            for ID in grouplist:
                group = {}
                group['sessionID'] = ID
                group['sessionName'] = self.getSessionByID(ID).get('sessionName',None)
                result.append(group)
        return result
    #以下四个函数，若没有消息，则返回None
    def get_session_last_time(self,sessionID):
        return self.getLastTime(sessionID)

    def get_session_last_message(self,sessionID):
        return self.getLastMessage(sessionID)

    def get_friend_last_time(self,username):
        friendSession = self.friendTable.get(username,None)
        if friendSession is None:
            return None
        else:
            return self.getLastTime(friendSession)

    def get_friend_last_message(self,username):
        friendSession = self.friendTable.get(username,None)
        if friendSession is None:
            return None
        else:
            return self.getLastMessage(friendSession)
            
        
    
    def test(self):
        pass
        #self.messageRecords[self.username] = [[datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '消息1']]
        #self.messageRecords[self.username] += [[datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '消息2']]

        # record1 = {'from':'5477','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'content':'hello'}
        # self.addRecordsDict("1",record1,None)
        # record3 = {'from':'5477','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'content':'hello'}
        # self.addRecordsDict("3",record3,None)
        # record2 = {'from':'8145','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'content':'nice'}
        # self.addRecordsDict("2",record2,'8145')
        # record3 = {'from':'5477','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'content':'hello'}
        # self.addRecordsDict("2",record3)
        # record4 = {'from':'8145','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'content':'nice'}
        # self.addRecordsDict("2",record4)
        # self.addRecordsDict("2",record4)

        # records = []
        # records.append(record1)
        # records.append(record2)
        # self.addRecordsDict("1",records)
        print(self.get_groups())
        print(self.get_session_last_time('4'))
        print(self.get_session_last_message('4'))
        # print(self.get_friend_last_time('8145'))
        # print(self.get_friend_last_message('8145'))
        # print("本地存储共有：",self.getSessionNum(),"个会话")
        # print("会话1有：",self.getRecordNum("1"),"条消息")
        # print("会话2最后消息时间：",self.getLastTime("2"))
        # print("会话2最后消息：",self.getLastMessage("2"))
        # print("输出会话2所有消息")
        # histories = self.getRecords("2",self.getRecordNum("2"))
        # for history in histories:
        #     print(history)
        # print("输出会话2最后5条消息")
        # histories = self.getRecords("2",5)
        # for history in histories:
        #     print(history)
    
    def close(self):
        self.messageRecords.close()
        
