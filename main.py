def test_data(data):
    from Common.base import User,UserMessage,Session
    avatar = "cd37c244-6558-42de-8fd4-770f75d1be8e"
    meaAvatar = "c1a33c9a-6de2-4ed9-91a1-d632f35865ca"
    mikoAvatar = "9ca418f1-2b37-42e6-962a-2a6e110b45c5"
    shionAvatar = "02862688-be78-42e9-9c51-2e06f534074c"
    matsuriAvatar = "116aba69-4727-41ad-948b-d4e6d98381ed"
    fubukiAvatar = "2e52793d-e18e-4591-bf2c-18099c61e88d"

    data['user'] = User('MinatoAqua', 'MinatoAqua', 'Aqua', avatar)

    mea = User('Mea', 'Mea', '昵称：mea', meaAvatar)
    miko = User('Miko', 'Miko', '昵称：miko', mikoAvatar)
    shion = User('Shion', 'Shion', '昵称：shion', shionAvatar)
    mazili = User('Mazili', 'Mazili', '昵称：matsuri', matsuriAvatar)
    xiaohuli = User('Xiaohuli', 'Xiaohuli', '昵称：fubuki', fubukiAvatar)
    fankangjun = User('fankangjun', 'fankangjun', '群名：反抗军', avatar)

    data['friendList'] = [mea, miko, shion, mazili, xiaohuli]
    data['groupList'] = [fankangjun]

    testUserMessage1 = UserMessage('Fubuki', '2020-5-26 15:13', 'KONKONKON', '0')
    testUserMessage2 = UserMessage('Fubuki', '2020-5-26 15:14', 'KONKONKON', '0')
    testUserMessage3 = UserMessage('Fubuki', '2020-5-26 15:15', 'KONKONKON', '0')
    testUserMessage4 = UserMessage('Fubuki', '2020-5-26 15:16', 'KONKONKON', '0')
    testUserMessage5 = UserMessage('Fubuki', '2020-5-26 15:17', 'KONKONKON', '0')
    data['sessions'] = [
        Session(233, [testUserMessage1, testUserMessage2, testUserMessage3, testUserMessage4, testUserMessage5])]
    session = data['sessions'][0]

    #print(session)

    data['search_result'] = None

if __name__ == '__main__':
    from BackEnd.BackEndThread import BackEndThread
    import multiprocessing
    mgr = multiprocessing.Manager()
    inner = {
    'user': {
        'version': '0',
        'username': '',
        'nickname': '',
        'avatarAddress': '',
        'phoneNumber': '',
        'email': '',
        'occupation': '',
        'invitee': '',
        'login_result':'-1',
        'login_information':'',
    },

    'friendList': {
        'version': '0',
        'list': []
    },

    'groupList': {
        'version': '0',
        'list': []
    },

    'usernameResult': {
        'version': '0',
        'list': []
    },

    'nicknameResult': {
        'version': '0',
        'list': []
    },
    
    'receiverList':{
        'version':'0',
        'list':[]
    },

    'requestorList':{
        'version':'0',
        'list':[]
    },
    
    'receiverMessage':{
        'version':'0',
        'receiverUsername':'',
        'avatarAddress':'',
        'result':'',
        'time':'',
    },
    
    'requestorMessage':{
        'version':'0',
        'requestorUsername':'',
        'avatarAddress':'',
        'checkMessage':'',
        'time':'',
    },
    
    'sessionList':{
        'version': '0',
        'list':[]
    }
}
    data = mgr.dict({
        "inner": inner,
        "write_lock":mgr.Lock()
    })
    RQ = multiprocessing.Queue()
    MQ = multiprocessing.Queue()
    bet = BackEndThread(RQ, MQ, data)
    
    bet.start()
    from Common.base import *
    pygame.init()
    pygame.key.set_repeat(500, 40)
    
    from FrontEnd.Processes.UserWindowProcess import UserWindowProcess as UWP
    from FrontEnd.Processes.LoginWindowProcess import LoginWindowProcess as LWP
    lwp = LWP(data, RQ, MQ, bet)
    lwp.run()

    lwp.close()

    #test_data(data)

    uwp = UWP(data, RQ, MQ, bet)
    uwp.run()
    bet.stop()
    bet.join()
    
    
    



    
