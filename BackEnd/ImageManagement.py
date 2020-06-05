import requests
import threading
import os
import sys
import pygame
def getLocalImage(imagePath):
    try:
        return pygame.image.load(imagePath)
    except:
        return None
def uploadImage(imagePath):
    imagename = None
    try:

        path = imagePath.decode('gbk')
        url = "http://121.199.55.52:8080/api/uploadImage"
        data = {'image' : open(path,'rb')}
        r = requests.post(url,files=data)
        response = r.json()
        imagename = os.path.split(response.get('data',None))[1]
    except Exception as e:
        print(e)
    return imagename

def downloadImage(imageName):
    thread = DownloadImageThread(imageName)
    thread.start()
    
    
class DownloadImageThread(threading.Thread):
    def __init__(self, imageName):
        threading.Thread.__init__(self)
        try:
            self.imageName = imageName
            self.url = "http://121.199.55.52:8080/api/image/"+imageName
            response = requests.get(self.url)
            img = response.content
            with open( "./images/"+imageName,'wb' ) as f:
                f.write(img)
        except Exception as e:
            print(e)

# nn = "52cca193-f879-4265-b3f5-d32d7e2248a4"
# downloadImage(imageName=nn)
# path = "C:/Users/dell/Desktop/Codes/FaceLook/BackEnd/userwindowbg.jpg"
# uploadImage(path)