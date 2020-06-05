from FrontEnd.Elements.Element import Element
from FrontEnd.Elements.Avatar import Avatar
from FrontEnd.Elements.CustomText import CustomText
from FrontEnd.Elements.SearchRightClick import SearchRightClick
from Common.base import readData
import pygame


class Title(Element):
    image_friend = pygame.image.load('./resources/UserWindowUI/search_friend.png')
    image_group = pygame.image.load('./resources/UserWindowUI/search_group.png')

    def __init__(self, process, location, title_type):
        Element.__init__(self, process)
        self.location = location
        if title_type == 0:
            self.surface = Title.image_friend
        elif title_type == 1:
            self.surface = Title.image_group


class ResultBlock(Element):
    # state==0 idle
    # state==1 hover
    # state==2 select
    # type==1 friend
    # type==2 group
    image = pygame.Surface((350, 100))
    image.fill((255, 255, 255))
    image_onHover = pygame.Surface((350, 100))
    image_onHover.fill((245, 245, 245))
    image_onClick = pygame.Surface((350, 100))
    image_onClick.fill((240, 240, 240))

    def __init__(self, process, location, user, block_type, menu):
        Element.__init__(self, process)
        self.user = user
        self.rightClickMenu = menu
        self.avatar = self.createChild(Avatar, (25, 15), user['avatarURL'])
        state = ' (online)' if user.state == 1 else ' (offline)'
        self.nicknameText = self.createChild(CustomText, (120, 38), 'dengxian', 25, (0, 0, 0), user['nickname'] + state)
        self.surface = ResultBlock.image
        self.location = location
        self.size = (350, 100)
        self.type = block_type
        self.frozen = False

    def pos_in(self, pos):
        x = pos[0]
        y = pos[1]
        if self.location[0] < x < self.location[0] + self.size[0] \
                and self.location[1] < y < self.location[1] + self.size[1]:
            return True
        return False

    def getEvent(self, event):
        if not self.frozen:
            if event.type == pygame.MOUSEMOTION and self.state != 2:
                if self.pos_in(event.pos):
                    self.state = 1
                    self.surface = ResultBlock.image_onHover
                else:
                    self.state = 0
                    self.surface = ResultBlock.image
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                if self.pos_in(event.pos):
                    if self.state == 2:
                        self.process.createSessionWindow(233)
                    else:
                        self.state = 2
                        self.surface = ResultBlock.image_onClick
                else:
                    self.state = 0
                    self.surface = ResultBlock.image
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT and self.pos_in(event.pos):
                self.rightClickMenu.change_location(event.pos)
                self.rightClickMenu.set_user(self.user)
                self.rightClickMenu.enable()


class SearchResult(Element):
    stupid_hint = pygame.image.load('./resources/UserWindowUI/support_to_search.png')

    def __init__(self, process, location):
        Element.__init__(self, process)
        self.disable()
        self.location = location
        self.surface = pygame.Surface((350, 550))
        self.surface.fill((220, 220, 220))
        self.blocks = []
        self.rightClickMenu = None
        self.index = 0
        self.refresh('')

    def refresh(self, keyword):
        self.blocks.clear()
        self.childs.clear()
        self.rightClickMenu = self.createChild(SearchRightClick)
        data = readData(self.process.data)
        if keyword == '':
            return
        self.blocks.append(self.createChild(Title, (0, 0), 0))
        index_ = 0
        try:
            for i in range(len(data['friendList'])):
                user = data['friendList'][i]
                if keyword in user['nickname'] or keyword in user['username']:
                    self.blocks.append(
                        self.createChild(ResultBlock, (0, index_ * 100 + 50), user, 1, self.rightClickMenu))
                    index_ += 1
            if index_ != 0:
                self.blocks.append(self.createChild(Title, (0, index_ * 100 + 50), 1))
                for i in range(len(data['groupList'])):
                    user = data['groupList'][i]
                    if keyword in user['nickname'] or keyword in user['username']:
                        self.blocks.append(
                            self.createChild(ResultBlock, (0, index_ * 100 + 100), user, 2, self.rightClickMenu))
                        index_ += 1
            else:
                self.blocks.append(self.createChild(Title, (0, 100), 1))
                for i in range(len(data['groupList'])):
                    user = data['groupList'][i]
                    if keyword in user['nickname'] or keyword in user['username']:
                        self.blocks.append(
                            self.createChild(ResultBlock, (0, index_ * 100 + 150), user, 2, self.rightClickMenu))
                        index_ += 1
        except KeyError:
            print('key error in SearchResult')

    def display(self):
        surface = self.surface.copy()
        blank = True
        for block in self.blocks:
            if block.active:
                blank = False
                surface.blit(block.display(), block.location)
        if blank:
            surface.blit(SearchResult.stupid_hint, (0, 0))
        if self.rightClickMenu.active:
            surface.blit(self.rightClickMenu.display(), self.rightClickMenu.location)
        return surface

    def getEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_WHEELDOWN and self.index <= len(self.blocks) - 7:
                self.index += 1
                for block in self.blocks:
                    block.location = (block.location[0], block.location[1] - 100)
            if event.button == pygame.BUTTON_WHEELUP and self.index > 0:
                self.index -= 1
                for block in self.blocks:
                    block.location = (block.location[0], block.location[1] + 100)

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        for child in self.childs:
            if child.active:
                child.getEvent(event)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            event.pos = (event.pos[0] + self.location[0], event.pos[1] + self.location[1])

    def update(self):
        if self.rightClickMenu.active:
            for block in self.blocks:
                block.frozen = True
        else:
            for block in self.blocks:
                block.frozen = False
        for child in self.childs:
            if child.active:
                child.update()
