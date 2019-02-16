from PIL import Image
import pytesseract 
import cv2
import os
import nltk


cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret,frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,5,3)
        gray = cv2.medianBlur(gray,3)
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename,gray)
        cv2.imshow("gray",gray)
        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)
        print(text)
        print("------------------")
        print([word for (word,pos) in nltk.pos_tag(nltk.word_tokenize(text)) if pos[0]== 'N'])
        if cv2.waitKey(60) == 27:
            break

cv2.destroyAllWindows()   
cap.release()