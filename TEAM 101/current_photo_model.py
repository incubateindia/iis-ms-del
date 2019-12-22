## a Deep Learning model to detect emotions 
## Input - Image File 
## Output - String Mood

import torch 
from torchvision import models
from torch import nn
from torchvision import transforms
from PIL import Image
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt 

class EmotionNet(object):

    def __init__(self):
        model = models.vgg16_bn()
        ## change the final layer
        final_in_feat = model.classifier[6].in_features
        model.classifier[6] =  nn.Linear(final_in_feat,500) ## number of output calsses
        model.classifier = nn.Sequential(*(model.classifier[i] for i in range(7)),
                                        nn.ReLU(),
                                        nn.Dropout(0.5),
                                        nn.Linear(500,6))

        self.model = model ## set up the model
        self.transform = transforms.Compose([transforms.Resize((224,224)),
                                 transforms.ToTensor(),
                                 transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
                                ]) ## set up the transform

        ## load the weights
        state_dict = torch.load('EmotionNet.pt',map_location=torch.device('cpu'))
        self.model.load_state_dict(state_dict)
        self.model.eval()

        ## Target Classes
        self.classes = ['Angry', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
        self.score = [5,4,1,2,3,2]

        ## harcasscade classifier
        self.face_clf = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')

    
    def detect_faces(self,img):
        face_img = img.copy() ## make a deep copy
        face_img_bg = cv2.cvtColor(face_img,cv2.COLOR_BGR2GRAY)
        face_rects = self.face_clf.detectMultiScale(face_img_bg,1.3,5)
        roi=None
        for (x,y,w,h) in face_rects:
            roi = face_img[y:y+h,x:x+w] ## region where face is
            roi = cv2.cvtColor(roi,cv2.COLOR_BGR2RGB)
        return roi

    def predict(self,image_path):
        img = cv2.imread(image_path) ## read the image
        roi = self.detect_faces(img) ## get the roi of image
        # plt.imshow(roi)
        # plt.show()

        image = Image.fromarray(roi)
        img_tensor = self.transform(image)
        img_tensor.unsqueeze_(0)

        output = self.model(img_tensor)

        _,labels = torch.max(output,1)
        label = self.classes[labels[0].item()]
        
        score = self.score[labels[0].item()]

        return label,score


if __name__ == '__main__':
    model = EmotionNet()
    print('Testing Image')
    output,score  = model.predict('./photo_uploads/1.jpg')
    print(output,score)