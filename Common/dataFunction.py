def readData(data):
    return data['inner']
def writeData(data,data_copy):
    data['write_lock'].acquire()
    data['inner'] = data_copy
    data['write_lock'].release()