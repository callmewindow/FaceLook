from BackEndThread import BackEndThread
import threading
import datetime
import json
import queue
from time import sleep

requestQueue = queue.Queue()
messageQueue = queue.Queue()
backend = BackEndThread(requestQueue,messageQueue)
backend.start()

logintest =  {"username": "hcz", "password": "123456", "messageNumber": "2"}
requestQueue.put(logintest)
# createsession = {"messageNumber": "6"}
# requestQueue.put(createsession)
#joinchat = {"messageNumber": "7","messageField1":"dsm","messageField2":"2"}
#requestQueue.put(joinchat)
# getfriendlsit = {"messageNumber": "4"}
# requestQueue.put(getfriendlsit)
# gethistory = {"messageNumber": "5"}
# requestQueue.put(gethistory)
# sleep(10)
# message = {'from':'hcz','to':None,'time':datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),'content':'hello dsm'}
# sendmessage = {"messageNumber": "9",'messageField1':'2','messageField2':json.dumps(message)}
# requestQueue.put(sendmessage)

sleep(10)
backend.stop()
backend.join()

while not messageQueue.empty():
    message = messageQueue.get()
    print(message)
