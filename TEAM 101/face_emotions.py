## a Deep Learning model to detect emotions 
## Input - Image File 
## Output - String Mood

from keras.models import load_model
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
from keras.preprocessing.image import img_to_array

from PIL import Image
import matplotlib.pyplot as plt

class EmotionNet(object):

    def __init__(self):
        model = load_model('EmotionNet.hdf5')

        self.model = model ## set up the model
        ## Target Classes
        emotion_dict= {'Angry': 0, 'Sad': 5, 'Neutral': 4, 'Disgust': 1, 'Surprise': 6, 'Fear': 2, 'Happy': 3}
        self.label_map = dict((v,k) for k,v in emotion_dict.items()) 
        self.score = [5,4,1,2,3,2]

        ## harcasscade classifier
        self.face_clf = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')

    
    def detect_faces(self,img):
    # Convert image to grayscale
        gray = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
        faces = self.face_clf.detectMultiScale(gray, 1.3, 5)
        if faces is ():
            return (0,0,0,0), np.zeros((48,48), np.uint8), img
        
        allfaces = []   
        rects = []
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation = cv2.INTER_AREA)
            allfaces.append(roi_gray)
            rects.append((x,w,y,h))
        return rects, allfaces, img

    def predict(self,image_path):
        img = cv2.imread(image_path) ## read the image
        rects, faces, image = self.detect_faces(img)
        total_score = 0
        emotion = []
        for face in faces:
            roi = face.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # make a prediction on the ROI, then lookup the class
            preds = self.model.predict(roi)[0]
            label = self.label_map[preds.argmax()]  
            emotion.append(label)
            total_score += self.score[preds.argmax()]
        return emotion,(total_score/len(faces))


if __name__ == '__main__':
    model = EmotionNet()
    print('Testing Image')
    output,score  = model.predict('./data/s2.jpg')
    print(output,score)