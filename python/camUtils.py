from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import imutils
import cv2
from threading import Thread, Semaphore
#from Counting import HandDetector
    
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    
    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.updated = True
        self.stream = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.stream.read()
        self.procFrame = imutils.resize(self.frame, width=400)
        self.sem = Semaphore(1) 
        self.name = "Cam"


        self.stopped = False
        #self.handDetector = HandDetector(min_detection_confidence=0.7)

    def startStream(self):

        print('starting')
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):

        print('updating')
        while True:
            
            if self.stopped:
                return       
            #self.sem.acquire()
            (self.grabbed, self.frame) = self.stream.read()
            self.updated = True
            #self.sem.release()

    def read(self):

        return self.frame
    
    def getFrame(self):
        return self.procFrame

    def stop(self):

        self._run_flag = False
        self.stopped = True
        self.wait()

    def run(self):
        print('Running')
        self.startStream()
        i = 0
        while self._run_flag:
            frame = self.read()
            frame = imutils.resize(frame, width=400)
            self.procFrame = frame
            #count = self.handDetector.countFingers(frame)
            #print(count)
            if True:
                self.change_pixmap_signal.emit(frame)
            #print('run')
        # shut down capture system
        #fps.stop()
        #print(i)
        #print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        #print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        self.stop()
    
    def isRunning(self):
        return self._run_flag
    
    def take(self):
        self.updated = False

    