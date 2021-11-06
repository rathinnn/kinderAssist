from ML import HandDetector
from ML import AttentionDetector, PresenceDetector
from threading import Thread
from imutils.video import FPS
currentOption = 2
currentNumber = 4

attentCode = {0:'Distracted', 1:'Sleeping', 2:'Good'}
class Process():
    def __init__(self, sio, vid, home):
        self.sio = sio
        self.vid = vid
        self.handDetector = HandDetector(min_detection_confidence=0.7)
        self.attentionDetector = AttentionDetector()
        self.presenceDetector = PresenceDetector()
        self.Counting = False
        self.present = True
        self.attent = 2
        self.home = home

        self.options = {1:self.optionFinger, 2:self.optionDistract, 3:self.optionPresence}

        
        @sio.on('update_option')
        def on_update(data):
            global currentOption
            print(data)
            currentOption = int(data[-1])
        
        @sio.on('updateNumber')
        def on_update(data):
            global currentNumber
            currentNumber = int(data['num'])
        


    def startStream(self):

        t = Thread(target=self.run, name='Process', args=())
        t.daemon = True
        t.start()
        return self



    def run(self):
        i = 0
        
        self.countfing = 0
        self.countatte = 0
        self.countpres = 0
        self.prevfing = self.Counting
        self.prevatte = self.attent
        self.prevpres = self.present
        #fps = FPS().start()
        while self.vid.isRunning():

            frame = self.vid.getFrame()
            frame2 = self.vid.read()

            curFunction = self.options[currentOption]

            if(currentOption == 1):
                curFunction(frame)
            
            else:
                curFunction(frame2)
    
        self.vid.stop()

    def updateFinger(self, sio, bool):
        sio.emit('wrong_counting', {'val': bool})
        self.setCount(bool)
    
    def updateDistract(self, sio, code):
        sio.emit('distracted', {'val': code})
        self.setDistract(code)
    
    def updatePresence(self, sio, bool):
        sio.emit('absent', {'val': not bool})
        self.setPresence(bool)

    
    def optionFinger(self, frame):
        counts = self.handDetector.countFingers(frame)
        print(counts)
        if(counts != currentNumber):
            count = True
        else:
            count = False
            
        if(self.countfing == 40 and count != self.Counting):
            self.Counting = count
            self.updateFinger(self.sio, count)

        if(count != self.prevfing):

            self.countfing = 0
            self.prevfing = count
        else:
            self.countfing += 1
    
    def setCount(self,count):
        if(count):
            self.home.dispAlert.setText("Wrong")
        
        else:
            self.home.dispAlert.setText("Correct")


    def optionDistract(self, frame):

        attent = self.attentionDetector.predict(frame)
        print(attent)
        
        if(self.countatte == 20 and attent != self.attent):
            self.attent = attent
            self.updateDistract(self.sio, attent)

        if(attent != self.prevatte):

            self.countatte = 0
            self.prevatte = attent
        else:
            self.countatte += 1
    
    def setDistract(self,attent):
        if(attent == 0):
            print("Student Distracted")
            self.home.dispAlert.setText("Student Distracted")
        
        elif (attent == 1):
            self.home.dispAlert.setText("Student Sleeping")
            print("Student Sleeping")
    
        else:
            self.home.dispAlert.setText("Welcome")
            print("Welcome")

    def optionPresence(self, frame):

        presence = self.presenceDetector.predict(frame)
        if(self.countpres == 80 and presence != self.present):
            self.present = presence
            self.updatePresence(self.sio, presence)

        if(presence != self.prevpres):

            self.countpres = 0
            self.prevpres = presence
        else:
            self.countpres += 1



    def setPresence(self,presence):
        if(presence):

            self.home.dispAlert.setText("Welcome")
            print(1)
        
        else:
            self.home.dispAlert.setText("Student Missing")
            print(0)



