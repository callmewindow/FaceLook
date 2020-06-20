class Element:
    def __init__(self, process):
        self.childs = []
        self.state = 0
        self.counter = 0
        self.surface = None
        self.process = process
        self.active = True
        self.data_version = 0
    def getEvent(self, event):
        for child in self.childs:
            if child.active:
                child.getEvent(event)

    def createChild(self, childType, *args, **kwargs):
        child = childType(self.process, *args, **kwargs)
        self.childs.append(child)
        return child

    def update(self):
        for child in self.childs:
            if child.active:
                child.update()

    def display(self):
        surface = self.surface.copy()
        for child in self.childs:
            if child.active:
                surface.blit(child.display(), child.location)
        return surface

    def switchState(self, state):
        self.state = state
        self.counter = 0

    def enable(self):
        self.active = True

    def disable(self):
        self.active = False

    def getMessage(self, message):
        pass