# -*- coding: utf-8 -*-
"""
this program will give a video feed 
a snapshot is captured
OCR will identified 'words' from the snapshot
the output words are sent to javascript somehow

"""
from re import sub
from string import punctuation
from nltk.corpus import words
from nltk import pos_tag
import time
import pytesseract
import cv2
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMessageBox, QMainWindow
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal,Qt
import numpy as np

cap = None
status = True
bgrImage = None


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    
    def run(self):
        global cap
        cap = cv2.VideoCapture(0)
        while True:
            ret,frame = cap.read()
            global bgrImage
            if status:
                bgrImage = frame
                if ret:
                    rgbImage = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    cvtToQtFormat = QImage(rgbImage.data,rgbImage.shape[1],rgbImage.shape[0], QImage.Format_RGB888)
                    p = cvtToQtFormat.scaled(640,480,Qt.KeepAspectRatio)
                    self.changePixmap.emit(p)
                    
class App(QMainWindow):
    def __init__(self):    
        super().__init__()
        self.title = 'Use Camera to Capture Words  | TSaurus- A learning App |'
        self.left= 100
        self.top= 100
        self.width= 680
        self.height= 560
        self.set_of_words = None
        self.initUI()
    
    @pyqtSlot(QImage)
    def setImage(self,image):
        self.label.setPixmap(QPixmap.fromImage(image))
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        #create a label which contains the video feed
        self.label = QLabel(self)
        self.label.move(20,20)
        self.label.resize(640,480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        button = QPushButton('Take a photo!',self)
        button.setToolTip('take a photo of some text, words will be extracted from the Photo!')
        button.move(300,510)
        button.clicked.connect(self.exit_)
        self.show()
        self.set_of_words = set(words.words())
        
    @pyqtSlot()
    def exit_(self):
        global status
        status = False
        #need to have best way to exit
        buttonReply = QMessageBox.question(self,'confirmation for exiting..','do you really wanna exit?',QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            print('Yes clicked')
            global bgrImage
            img = cv2.resize(bgrImage, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(bgrImage, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((1,1),np.uint8)
            img = cv2.dilate(img,kernel,iterations=1)
            img = cv2.erode(img, kernel, iterations=1)
            img = cv2.GaussianBlur(img, (5,5), 0)
#            img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            img = cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,7, 2)
#            img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 2)
            while True:
                cv2.imshow("img",img)
                if cv2.waitKey(60)==27:
                    break
            result = []
            text = (pytesseract.image_to_string(img,lang="eng")).lower()
            text = sub('['+punctuation+']',' ',text).split()
            for textWord in text:
                if textWord in self.set_of_words:
                    result.append(textWord)
            result = pos_tag(result)                    
            nouns = [word for word,pos in result if (pos == 'NN' or pos == 'NNP')]
            print(nouns)
            #print([word for (word,pos) in nltk.pos_tag(nltk.word_tokenize(result)) if pos[0]== 'N'])
            #something wrong. only right words are not filtered. all are displayed.
            #study ordereddict implement that
            time.sleep(10)
            global cap
            cap.release()
            cv2.destroyAllWindows()
            print("done")
            sys.exit(app.exec_())
        else:
            print('No clicked')
            status = True

app= QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())
    
#___________________________________
#___________________________________
comment ="""
    Also available from Vintage
Haruki Murakami

AFTER THE QUAKE |

“How does Murakami} “he cieieas
am manage to make pactry while writing
or contemporary life and emotions? | am weakekeeced With
admiration®
Independent an Sunday
Bremin the dipperiest af ste Murakaint'e torics, unre

of drrait Nash nue warm with lite’ ;
________________________
['Vintage', 'Haruki', 'Murakami', 'AFTER', 'THE', 'QUAKE', '“', 'How',
 'Murakami', 'manage', 'writin', 'life', 'emotions', 'sh', 'admiration', '”',
 'Jadependent', 'Sunday', '‘', 'slipperiest', 'Me', 'Murakami', 'stunics', 
 'PF', 'detzit', 'flash', 'New', 'York', 'Times', 'cxonomy', 'Peuple', 'bee', 'Heh', 'thes', 'scabs']



KeyboardInterrupt
"""

    