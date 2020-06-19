def lockData(data):
    data['write_lock'].acquire()
def unlockData(data):
    data['write_lock'].release()
def readData(data):
    lockData(data)
    dat = data['inner']
    unlockData(data)
    return dat
def writeData(data,data_copy):
    data['inner'] = data_copy