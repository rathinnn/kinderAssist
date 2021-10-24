import mediapipe as mp
import cv2
import math
import numpy as np


#Initializations: static code
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils



class HandDetector:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        #when the mediapipe is first started, it detects the hands. After that it tries to track the hands
        #as detecting is more time consuming than tracking. If the tracking confidence goes down than the
        #specified value then again it switches back to detection
        self.hands = mpHands.Hands(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence,
                                   min_tracking_confidence=min_tracking_confidence)


    def findHandLandMarks(self, image, handNumber=0, draw=False):
        originalImage = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # mediapipe needs RGB
        results = self.hands.process(image)
        landMarkList = []

        if results.multi_handedness:
            label = results.multi_handedness[handNumber].classification[0].label  # label gives if hand is left or right
            #account for inversion in webcams
            if label == "Left":
                label = "Right"
            elif label == "Right":
                label = "Left"


        if results.multi_hand_landmarks:  # returns None if hand is not found
            hand = results.multi_hand_landmarks[handNumber] #results.multi_hand_landmarks returns landMarks for all the hands

            for id, landMark in enumerate(hand.landmark):
                # landMark holds x,y,z ratios of single landmark
                imgH, imgW, imgC = originalImage.shape  # height, width, channel for image
                xPos, yPos = int(landMark.x * imgW), int(landMark.y * imgH)
                landMarkList.append([id, xPos, yPos, label])

            if draw:
                mpDraw.draw_landmarks(originalImage, hand, mpHands.HAND_CONNECTIONS)

        return landMarkList

    def countFingers(self, image):

        
        handLandmarks = self.findHandLandMarks(image=image, draw=False)
        count=0

        if(len(handLandmarks) != 0):
            #we will get y coordinate of finger-tip and check if it lies above middle landmark of that finger
            #details: https://google.github.io/mediapipe/solutions/hands

            if handLandmarks[4][3] == "Right" and handLandmarks[4][1] > handLandmarks[3][1]:       #Right Thumb
                count = count+1
            elif handLandmarks[4][3] == "Left" and handLandmarks[4][1] < handLandmarks[3][1]:       #Left Thumb
                count = count+1
            if handLandmarks[8][2] < handLandmarks[6][2]:       #Index finger
                count = count+1
            if handLandmarks[12][2] < handLandmarks[10][2]:     #Middle finger
                count = count+1
            if handLandmarks[16][2] < handLandmarks[14][2]:     #Ring finger
                count = count+1
            if handLandmarks[20][2] < handLandmarks[18][2]:     #Little finger
                count = count+1

        return count



class AttentionDetector():
    def __init__(self):


        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')



        
    def predict(self, img): 
        faceBool = True
        eyesBool = True
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        gray = cv2.bilateralFilter(gray,5,1,1)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5,minSize=(200,200)) 
        for (x,y,w,h) in faces: 
            #img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),10) 
            roi_gray = gray[y:y+h, x:x+w] 
            roi_color = img[y:y+h, x:x+w] 
            eyes = self.eye_cascade.detectMultiScale(img,1.3,5,minSize=(50,50))
            #for (ex,ey,ew,eh) in eyes: 
                #img = cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,0,255),2) 
            if(len(eyes)>=2):
                pass
            else:
                eyesBool = False
        
        if(len(faces) == 0):
            return 0

        if (faceBool and eyesBool):
            return 2
        
        if (faceBool and not eyesBool):
            return 1


class PresenceDetector():

    def __init__(self):

        self.face_detection = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)


    def predict(self, image):
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(image)
        if results.detections:
            return True
        
        return False
