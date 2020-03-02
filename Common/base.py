from sys import exit
def panic():
    raise Exception()
class Action():
    pass
class CreateAction(Action):
    def __init__(self,sessionID):
        pass
class Message():
    def __init__(self,type,content):
        pass
    
    def toString(self):
        pass