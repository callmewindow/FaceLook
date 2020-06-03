import shelve
import datetime
import os
import json


class LocalStorage(object):
    def __init__(self, username):
        self.username = username
        self.messageRecords = None
        new = False
        if not os.path.exists("./"+username):
            os.mkdir("./"+self.username)
            new = True
        os.chdir("./"+username)
        self.messageRecords = shelve.open("messageRecords",writeback=True)
        self.sessionTable = shelve.open("sessionTable",writeback=True)
        if new:
            self.sessionTable['num_of_session'] = 0


    def addSession(self,sessionID):
        #在存储中新建会话
        tableItem = self.sessionTable.get(sessionID,None)
        if tableItem == None:
            self.messageRecords[sessionID] = []
            addNum = {'num_of_session':self.sessionTable['num_of_session']+1}
            self.sessionTable.update(addNum)
            self.sessionTable[sessionID] = {
                'num_of_message' : 0,
                'last_time' : None,
                'last_message' : None
            }


    def addRecordsDict(self,sessionID,records):
        #向存储中添加消息
        #参数records可为dict或list(dict)
        tableItem = self.sessionTable.get(sessionID,None)
        if tableItem == None:
            self.messageRecords[sessionID] = []
            addNum = {'num_of_session':self.sessionTable['num_of_session']+1}
            self.sessionTable.update(addNum)
            self.sessionTable[sessionID] = {
                'num_of_message' : 0,
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

    def rewriteRecord(self,sessionID,records):
        #用records覆盖某会话的存储
        #records为list
        tableItem = self.sessionTable.get(sessionID,None)
        if tableItem == None:
            addNum = {'num_of_session':self.sessionTable['num_of_session']+1}
            self.sessionTable.update(addNum)
        self.messageRecords[sessionID] = []
        self.sessionTable[sessionID] = {
            'num_of_message' : 0,
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
            
        
    
    def test(self):
        #self.messageRecords[self.username] = [[datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '消息1']]
        #self.messageRecords[self.username] += [[datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '消息2']]

        # record1 = {'from':'5477','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'content':'hello'}
        # self.addRecordsDict("1",record1)
        # record2 = {'from':'8145','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'content':'nice'}
        # self.addRecordsDict("1",record2)
        # record3 = {'from':'5477','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'content':'hello'}
        # self.addRecordsDict("2",record3)
        # record4 = {'from':'8145','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'content':'nice'}
        # self.addRecordsDict("2",record4)
        # self.addRecordsDict("2",record4)

        # records = []
        # records.append(record1)
        # records.append(record2)
        # self.addRecordsDict("1",records)

        print("本地存储共有：",self.getSessionNum(),"个会话")
        print("会话2有：",self.getRecordNum("2"),"条消息")
        print("会话2最后消息时间：",self.getLastTime("2"))
        print("会话2最后消息：",self.getLastMessage("2"))
        print("输出会话2所有消息")
        histories = self.getRecords("2",self.getRecordNum("2"))
        for history in histories:
            print(history)
        print("输出会话2最后5条消息")
        histories = self.getRecords("2",5)
        for history in histories:
            print(history)
    
    def close(self):
        self.messageRecords.close()
        

# local = LocalStorage("hcz")
# local.test()
# local.close()

