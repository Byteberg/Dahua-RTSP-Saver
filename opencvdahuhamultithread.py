import cv2
import time
import queue
import numpy
import threading

CHANNELSELECT = "1"
STREAMSELECT = "0"
USERNAME = "admin"
PASSWORD = "adminpw"
ADDRESS = "192.168.1.32:554"
live_resoltion_1 = 500
live_resoltion_2 = 500



class dahua_stream_multithreaded():
    queobj = ""
    threadobj = ""
    captureobj = ""
    def __init__(self,USERNAME,PASSWORD,ADDRESS,CHANNELSELECT,STREAMSELECT,buffer_size_int):
        threadobjj = threading.Thread(target=get_frames, daemon=True)
        threadobjj.start()

    def get_frames(self):
        while True:
            try:
                self.queobj.put(self.captureobj.read()[1],timeout=1)
                #pipeobj.put(capture.read()[1], timeout=0)
            except Exception as X:
                print(X)
                print("que full" + str(time.asctime()))

    def gen_queue(self,buffer_size_int):
        self.queobj = queue.Queue(buffer_size)

    def start_video_cap(self,USERNAME,PASSWORD,ADDRESS,CHANNELSELECT,STREAMSELECT,):
        self.captureobj =capture = cv2.VideoCapture(str("rtsp://" + USERNAME + ":" + PASSWORD + "@" + ADDRESS + '/cam/realmonitor?channel=' + CHANNELSELECT + '&subtype=' + STREAMSELECT))

    def close_obj(self):
        del self.captureobj
        self.threadobj.close()
        self.captureobj.release()

capture.read()[1]



captureobj = dahua_stream_multithreaded(USERNAME,PASSWORD,ADDRESS,CHANNELSELECT,STREAMSELECT,5)



while True:

    #frame = capture.read()[1]
    frame = captureobj.queobj.get()

    try:

        frame = cv2.resize(frame,(1000,1000))
        cv2.imshow(str(ADDRESS),frame)
        
        cv2.waitKey(1)
    except Exception as X:
        print(X)


