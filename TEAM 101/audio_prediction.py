import glob 
import keras
import librosa
import numpy as np
import pandas as pd
import os

from keras.models import model_from_json
from sklearn.preprocessing import LabelEncoder

def loadModel():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("saved_models/Emotion_Voice_Detection_Model.h5")
    return loaded_model

def audio_predict(path):
    loaded_model = loadModel()
    print("Loaded model from disk")
    
    lb = LabelEncoder()
    lb.fit(["female_angry", "female_calm", "female_fearful", "female_happy", "female_sad", "male_angry", "male_calm", "male_fearful", "male_happy", "male_sad"])
    
    # Preprocess audio file
    X, sample_rate = librosa.load(path, res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
    sample_rate = np.array(sample_rate)
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=13),axis=0)
    featurelive = mfccs
    livedf2 = featurelive
    livedf2= pd.DataFrame(data=livedf2)
    livedf2 = livedf2.stack().to_frame().T
    twodim= np.expand_dims(livedf2, axis=2)
    
    livepreds = loaded_model.predict(twodim, 
                         batch_size=32, 
                         verbose=1)
    livepreds1=livepreds.argmax(axis=1)
    liveabc = livepreds1.astype(int).flatten()
    livepredictions = (lb.inverse_transform((liveabc)))
    dictionary={
    "female_angry" : 5, 
    "female_calm" : 2, 
    "female_fearful" :4, 
    "female_happy" : 1, 
    "female_sad" :3, 
    "male_angry" : 5, 
    "male_calm": 2, 
    "male_fearful" : 4, 
    "male_happy" : 1, 
    "male_sad": 1
    }
    keras.backend.clear_session()
    return str(dictionary[livepredictions[0]])

# print(predict('./audio_uploads/sa13.wav'))
