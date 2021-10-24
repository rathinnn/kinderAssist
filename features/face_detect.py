import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml') 

return_var = 0

cap = cv2.VideoCapture(0) 
while 1: 
    ret, img = cap.read() 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    gray = cv2.bilateralFilter(gray,5,1,1)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5,minSize=(200,200))
    if(len(faces)>0):
        for (x,y,w,h) in faces: 
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),10) 
            roi_gray = gray[y:y+h, x:x+w] 
            roi_color = img[y:y+h, x:x+w] 
            eyes = eye_cascade.detectMultiScale(img,1.3,5,minSize=(50,50)) 
            for (ex,ey,ew,eh) in eyes: 
                img = cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,0,255),2) 
            if(len(eyes)>=2):
                pass
            else:
                return_var = 1
    else:
        return_var = 1
    


    print(return_var)

    cv2.imshow('img',img) 
    k = cv2.waitKey(30) & 0xff
    if k == 27: 
        break
cap.release() 
cv2.destroyAllWindows() 