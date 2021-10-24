from ML import HandDetector
from ML import AttentionDetector, PresenceDetector
from threading import Thread
from imutils.video import FPS
currentOption = 1
currentNumber = 4

attentCode = {0:'Distracted', 1:'Sleeping', 2:'Good'}
class Process():
    def __init__(self, sio, vid):
        self.sio = sio
        self.vid = vid
        self.handDetector = HandDetector(min_detection_confidence=0.7)
        self.attentionDetector = AttentionDetector()
        self.presenceDetector = PresenceDetector()
        self.Counting = True
        self.present = True
        self.attent = 2
        
        @sio.on('updateOption')
        def on_update(data):
            global currentOption
            currentOption = data
        
        @sio.on('updateNumber')
        def on_update(data):
            global currentNumber
            currentNumber = data
        


    def startStream(self):

        t = Thread(target=self.run, name='Process', args=())
        t.daemon = True
        t.start()
        return self



    def run(self):
        i = 0
        
        countfing = 0
        countatte = 0
        countpres = 0
        prevfing = self.Counting
        #fps = FPS().start()
        while self.vid.isRunning():
            #fps._numFrames < 100:
            #
            #self.vid.sem.acquire()
            frame = self.vid.getFrame()
            frame2 = self.vid.read()
            #self.vid.sem.release()
            count = self.handDetector.countFingers(frame)
            #attent = self.attentionDetector.predict(frame2)
            #presence = self.presenceDetector.predict(frame2)

            if(countfing == 60 and count != self.Counting):
                self.Counting = count
                print(count)
                #updateFinger(self.sio, count)

            if(count != prevfing):
                countfing = 0
                prevfing = count
            else:
                countfing += 1

            

            
            #fps.update()

            #print(presence)
            #print(attentCode[attent])
            #if(count != currentNumber):
            #    print('Not Equal')
        # shut down capture system
        #fps.stop()
        #print(i)
        #print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        #print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        #fps.stop()
        #print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        #print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        self.vid.stop()

    def updateFinger(sio, bool):
        sio.emit('wrong_counting', {'val': str(bool)})
    
    def updateDistract(sio, code):
        sio.emit('distracted', {'val': str(code)})
    
    def updatePresence(sio, bool):
        sio.emit('absent', {'val': str(not bool)})

