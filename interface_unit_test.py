import traceback
#from Common.base import *
from multiprocessing import Queue
from BackEnd.BackEndThread import BackEndThread
from time import sleep
from interface_sample import *
import sys
import datetime
RQ = Queue()
MQ = Queue()
bet = BackEndThread(RQ,MQ)
message = None
def sendRequest(request):
    RQ.put(request)
    message = None
    print('[Unit Test] Request put.')
    try:
        message = MQ.get(timeout=5)
    except:
        print(traceback.print_exc())
    if message:
        print('[Unit Test Message]',message)
def flush():
    message = None
    go = True
    print('[Flush Start]')
    while go:
        try:
            message = MQ.get(timeout=1)
            print('[Flush Message]',message)
        except:
            go = False
    print('[Flush End]')
def start():
    bet.start()
def login(username,password):
    r = login_request
    r['username']=username
    r['password']=password
    sendRequest(r)
def register():
    r = register_request
    sendRequest(r)
def get_friend_list():
    r = get_friend_list_request
    sendRequest(r)
def remove_friend():
    r = remove_friend_request
    sendRequest(r)
def get_history_message():
    r = get_history_message_request
    sendRequest(r)
def create_session(sessionName):
    r = create_session_request
    r['sessionName']=sessionName
    sendRequest(r)
def take_user_into_session(username,sessionId):
    r = take_user_into_session_request
    r['username']=username
    r['sessionId']=sessionId
    sendRequest(r)
def edit_profile():
    r = edit_profile_request
    sendRequest(r)
def get_notice():
    r = get_notice_request
    sendRequest(r)
def exit():
    bet.stop()
    bet.join()
    sys.exit()

    

# 测试
