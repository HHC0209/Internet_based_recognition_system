import requests
import json
from datetime import datetime
from PyQt5.Qt import QThread,QMutex,pyqtSignal
from PyQt5.QtCore import QSettings
from pygame import time

def get_emotion(txt_path="example.txt"):
    with open(txt_path, 'r') as file:
        content_list = file.readlines() 
    content_list = json.dumps(content_list)
    payload = {"user_id": "002", "eeg": content_list}  
    request_url = "http://8.129.167.99:5000/predict"
    result = ""

    try:
        res = requests.post(request_url, data=payload)
        if res.status_code == requests.codes.ok:
            res = json.loads(str(res.text))
            if res["success"]:
                result = res["emotion"]
        else:
            print("Network Error in emotion request")
    except:
        print("Network Error in emotion request")

    return result

def get_music(txt_path="example.txt"):
    with open(txt_path, 'r') as file:
        content_list = file.readlines() 
    content_list = json.dumps(content_list)
    payload = {"user_id": "004", "eeg": content_list}  
    request_url = "http://8.129.167.99:5000/generate"

    try:
        # Origin code to request music
        # res = requests.post(request_url, data=payload)
        # if res.status_code == requests.codes.ok:
        #     mid_path = r"music\\" + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".mid"
        #     with open(mid_path, "wb") as conf:
        #         conf.write(res.content)
        # else:
        #     mid_path = ""
        #     print("Network Error in music request")
        
        # random choose music from local
        time.wait(2000)
        settings = QSettings("Config.ini", QSettings.IniFormat)
        current = int(settings.value("current"))
        total = int(settings.value("total"))
        mid_path = r"music\\" + str(current) + ".mid"
        current = (current + 1) % total
        settings.setValue("current", current)
        settings.sync()
    except:
        mid_path = ""
        print("Network Error in music request")

    return mid_path

class Music(QThread):
    trigger = pyqtSignal(str)
    def __init__(self, txt_path):
        super().__init__()
        self.txt_path = txt_path
        
    def run(self):
        print("start music request thread")
        mid_path = get_music(self.txt_path)
        self.trigger.emit(mid_path)

class Emotion(QThread):
    trigger = pyqtSignal(str)
    def __init__(self, txt_path):
        super().__init__()
        self.txt_path = txt_path

    def run(self):
        print("start emotion request thread")
        emotion = get_emotion(self.txt_path)
        self.trigger.emit(emotion)