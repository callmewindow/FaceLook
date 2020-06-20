from FrontEnd.Elements.SearchWindow import SearchWindow
from FrontEnd.Processes.WindowProcessWithoutQueue import WindowProcessWithoutQueue


class SearchWindowProcess(WindowProcessWithoutQueue):
    def __init__(self, data, RQ, MQ):
        self.data = data

        WindowProcessWithoutQueue.__init__(self, data, RQ, MQ, None, SearchWindow(self))


def createSearch(data, RQ, MQ):
    swp = SearchWindowProcess(data, RQ, MQ)
    swp.run()
