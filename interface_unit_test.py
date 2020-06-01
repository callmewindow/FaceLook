import traceback
from Common.base import *
from BackEnd.BackEndThread import BackEndThread
from time import sleep
RQ = Queue()
MQ = Queue()
bet = BackEndThread(RQ,MQ)
try:
    message = None
    bet.start()
    request = {
        'messageNumber':'2',
        'messageField1':'hcz',
        'messageField2':'123456'
        }
    RQ.put(request)
    print('[Unit Test] Request put.')
    message = MQ.get(timeout=5)
    print('[Unit Test Message]',message)
except Exception as e:
    print('[Unit Test Error]:')
    print(e)    
finally:
    sleep(5)
    bet.stop()
    bet.join()
    if message == None:
        print('Time Out!')
