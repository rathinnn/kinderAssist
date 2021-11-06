import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from camUtils import VideoThread
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import cv2
import requests
from processImage import Process
from client import sio

class LoginScreen(QDialog):
    def __init__(self, widget):
        super(LoginScreen, self).__init__()
        loadUi("login.ui",self)
        self.closeBtn.clicked.connect(lambda:widget.close())
        self.loginBtn.clicked.connect(lambda:self.login(widget))

    
    def login(self, widget):
        
        username = self.username.text()
        password = self.password.text()
        if len(username)==0 or len(password)==0:
            self.error.setText("Please input all fields.")
            return False
        elif not self.authenticate(username, password):
            self.error.setText("Wrong Username or Password")
            return False
        print("Succesful")
        home = Home(self.loggedUsername, self.session_id)
        widget.addWidget(home)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setStyleSheet('#wind{background-image: url(pyBack.png); background-position: center;}')
        widget.setFixedHeight(958)
        widget.setFixedWidth(1525)
        self.centerWidgetOnScreen(widget)
        widget.setWindowFlags(QtCore.Qt.Window)
        widget.show()

        return True
        

    
    def centerWidgetOnScreen(self, widget):
        centerPoint = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        fg = widget.frameGeometry()
        fg.moveCenter(centerPoint)
        widget.move(fg.topLeft())
    
    def authenticate(self, username, password):
        curSession = requests.Session() 
        #print(username)
        #print(password)
        response = curSession.post("http://localhost:8080/login", data={'username': username, 'password': password})
        #print(response.status_code)
        #print(response.text)
        if response.status_code == 401:
            self.error.setText("Invalid username or password")
            return False

        response2 = curSession.get("http://localhost:8080/socket_token/")
        #print(response2.status_code)
        response2 = response2.json()
        #print(response2)
        self.loggedUsername = response2['username']
        self.session_id = response2['session_id']
        #self.loggedUsername = 'adfads'
        #self.session_id = 'asdfsadfasd'
        self.error.setText("")
        return True

    


    


class Home(QDialog):
    def __init__(self, username, session_id):
        super(Home, self).__init__()
        loadUi("home.ui",self)

        self.authe = {'username' : username, 'session_id' : session_id, 'profession': 'student'}
        #print(username)
        sio.connect('http://localhost:8080', auth = self.authe)
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()
        self.username = username
        self.session_id = session_id
        self.process = Process(sio, self.thread, self)
        self.process.startStream()
        
        

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(400, 400, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


# main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
welcome = LoginScreen(widget)
widget.addWidget(welcome)
widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
widget.setFixedHeight(800)
widget.setFixedWidth(1000)
welcome.centerWidgetOnScreen(widget)


widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
    sio.disconnect()