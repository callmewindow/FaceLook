from FrontEnd.Elements.Window import Window
from FrontEnd.Elements.UserWindowBackground import UserWindowBackground


class UserWindow(Window):
    def __init__(self, process):
        Window.__init__(self, process, 'FaceLook!', (350, 740), (255, 255, 255), True)
        self.bg = self.createChild(UserWindowBackground)
        self.set_rounded_rectangle(20)
        self.need_session = False
        self.needed_username = ''
        self.set_location((1400, 200))
        self.heartbeat = 0

    def update(self):
        # keepalive
        self.heartbeat += 1
        if self.heartbeat == 3600:
            self.process.requestQueue.put({'messageNumber': '5'})
            self.heartbeat = 0
        for child in self.childs:
            if child.active:
                child.update()

    '''def getMessage(self, message):
        data = readData(self.process.data)

        # 获取好友列表
        try:
            if message['messageNumber'] == '4r':
                data['friendList'] = message['friendlist']
                writeData(self.process.data, data)
                # 这玩意儿是让前端好友列表刷新，包括好友数量、昵称、头像，新机制下不需要了
                self.bg.friend_list.refresh()
                #
                return
        except KeyError:
            print('key error in 4r')

        # 获取会话列表
        try:
            if message['messageNumber'] == '5r':
                # 这玩意儿是让前端好友列表的最新消息、群聊列表的最新消息刷新，新机制下不需要了
                self.bg.friend_list.update_info()
                self.bg.group_list.update_info()
                #
                return
        except KeyError:
            print('key error in 5r')

        # 创建会话
        try:
            if message['messageNumber'] == '6r':
                # need_session与12r联动
                if self.need_session:
                    # 如果need_session，即刚刚通过了一个好友请求，那么把这个好友加入刚申请到的无名session中，发5号请求刷新列表
                    self.need_session = False
                    self.process.requestQueue.put({'messageNumber': '7',
                                                   'username': self.needed_username,
                                                   'sessionId': message['sessionId']})
                    self.process.requestQueue.put({'messageNumber': '5'})
                else:
                    # 否则说明刚申请到的session是群聊，那么只发5号请求刷新列表
                    self.process.requestQueue.put({'messageNumber': '5'})
                    sleep(1)
                    self.bg.group_list.refresh()
                #
                return
        except KeyError:
            print('key error in 6r')

        # 获取未处理好友申请列表
        try:
            if message['messageNumber'] == '8r':
                # 单纯塞数据
                data['requestorList'] = message['requestorList']
                writeData(self.process.data, data)
                #
                return
        except KeyError:
            print('key error in 8r')

        # 收到聊天消息
        try:
            if message['messageNumber'] == '9r':
                # 这里原意是收到9r说明有新消息，直接发5号请求获取新的消息列表
                # 但9r包含了该条消息的全部，新机制下9r可以被用于直接更新相关列表，向list中插入
                self.process.requestQueue.put({'messageNumber': '5'})
                #
                return
        except KeyError:
            print('key error in 9r')

        # 好友申请消息（服务端==>接收方）（仅限接收方在线）
        try:
            if message['messageNumber'] == '11r':
                # 11r为通知性消息，告知前端有新请求，需要显示一个小红点，新机制下实际上只需要维护版本号即可
                self.bg.main_menubar.apply_button.notice = True
                #
                return
        except KeyError:
            print('key error in 11r')

        # 回复好友申请（接收方==>服务端）
        try:
            if message['messageNumber'] == '12r' and message['result'] == '1':
                # 如果12r的result是1，说明“我”通过了好友请求，服务器上的好友列表被修改了，需要发送4号请求获取新的好友列表
                # 同时，因为新好友需要一一对应的新sessionId，故此处自动标记need_session，与6r联动
                self.need_session = True
                self.needed_username = message['requestorUsername']
                self.process.requestQueue.put({'messageNumber': '4'})
                #
                return
        except KeyError:
            print('key error in 12r')

        # 好友申请回复结果（服务端==>申请方）（仅限申请方在线）
        try:
            if message['messageNumber'] == '13r':
                # 如果13r的result是1，说明好友请求被通过，服务器上的好友列表被修改了，需要发送4号请求获取新的好友列表
                if message['result'] == '1':
                    self.process.requestQueue.put({'messageNumber': '4'})
                return
                #
        except KeyError:
            print('key error in 13r')

        # 获取申请结果列表
        try:
            if message['messageNumber'] == '14r':
                # 单纯塞数据，按照新的data格式来
                data['receiverList'] = message['receiverList']
                writeData(self.process.data, data)
                #
                return
        except KeyError:
            print('key error in 14r')

        # 删除好友（A==>服务端）
        try:
            if message['messageNumber'] == '15r':
                # 收到15r说明服务器上的好友列表被修改了，需要发送4号请求获取新的好友列表
                self.process.requestQueue.put({'messageNumber': '4'})
                #
                return
        except KeyError:
            print('key error in 15r')

        # 删除好友（服务端==>B）
        try:
            if message['messageNumber'] == '16r':
                # 收到16r说明服务器上的好友列表被修改了，需要发送4号请求获取新的好友列表
                self.process.requestQueue.put({'messageNumber': '4'})
                #
                return
        except KeyError:
            print('key error in 16r')

        # 退出群聊
        try:
            if message['messageNumber'] == '17r':
                # 收到17r说明服务器上的群聊消息被修改了，需要发送5号请求获取新的session列表
                self.process.requestQueue.put({'messageNumber': '5'})
                #
                return
        except KeyError:
            print('key error in 17r')

        # 更改个人信息
        try:
            if message['messageNumber'] == '18r':
                # 把新的个人信息塞进data，没啥好说的
                data['user'] = {
                    'username': data['user']['username'],
                    'nickname': message['nickname'],
                    'avatarAddress': message['avatarAddress'],
                    'phoneNumber': message['phoneNumber'],
                    'invitee': message['invitee'],
                    'email': message['email'],
                    'occupation': message['occupation'],
                    'location': message['location'],
                }
                #
                writeData(self.process.data, data)
                # 让前端刷新个人资料，类似qq最上面那块，新机制下已不需要
                self.bg.self_info.refresh()
                #
                return
        except KeyError:
            print('key error in 18r')

        # 修改群聊信息
        try:
            if message['messageNumber'] == '19r':
                # 收到19r说明服务器上的群聊消息被修改了，需要发送5号请求获取新的session列表
                self.process.requestQueue.put({'messageNumber': '5'})
                #
                return
        except KeyError:
            print('key error in 19r')

        # 按昵称搜好友
        try:
            if message['messageNumber'] == '20r':
                # 塞数据
                data['search_nickname'] = message['userlist']
                writeData(self.process.data, data)
                return
        except KeyError:
            print('key error in 20r')

        # 按用户名搜好友
        try:
            if message['messageNumber'] == '21r':
                # 塞数据
                data['search_username'] = message['userlist']
                writeData(self.process.data, data)
        except KeyError:
            print('key error in 21r')'''
