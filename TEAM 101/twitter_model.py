import warnings
warnings.filterwarnings("ignore")
import ftfy
import nltk
import numpy as np
import pandas as pd
import re
from math import exp
from numpy import sign

from gensim.models import KeyedVectors
from nltk.corpus import stopwords
from nltk import PorterStemmer

import keras
from keras.models import Model, Sequential
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import Conv1D, Dense, Input, LSTM, Embedding, Dropout, Activation, MaxPooling1D
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer




class TwitterModel(object):

    def __init__(self):
        self.MAX_SEQUENCE_LENGTH = 140 # Max tweet size
        self.MAX_NB_WORDS = 20000
        self.EMBEDDING_DIM = 300
        self.DEPRESSIVE_TWEETS_CSV = 'depressive_tweets_processed.csv'
        self.DEPRES_NROWS = 3200  # number of rows to read from DEPRESSIVE_TWEETS_CSV
        self.RANDOM_NROWS = 8000 # number of rows to read from RANDOM_TWEETS_CSV
        self.model = load_model('./TwitterModel.h5')
        self.c_re = self.preprocess()
        depressive_tweets_df = pd.read_csv(self.DEPRESSIVE_TWEETS_CSV, sep = '|', header = None, usecols = range(0,9), nrows = self.DEPRES_NROWS)
        tweet_df = pd.read_csv('sentiment_tweets3.csv')
        random_tweet_df = tweet_df[tweet_df['label']==0]
        depressive_tweets_arr = [x for x in depressive_tweets_df[5]]
        random_tweets_arr = [x for x in random_tweet_df['message']]
        X_d = self.clean_tweets(depressive_tweets_arr)
        X_r = self.clean_tweets(random_tweets_arr)
        tokenizer = Tokenizer(num_words=self.MAX_NB_WORDS)
        tokenizer.fit_on_texts(X_d + X_r)
        self.tokenizer = tokenizer
        self.sentiment = SentimentIntensityAnalyzer() 



    def preprocess(self):
        # Expand Contraction
        self.cList  = {
            "ain't": "am not",
            "aren't": "are not",
            "can't": "cannot",
            "can't've": "cannot have",
            "'cause": "because",
            "could've": "could have",
            "couldn't": "could not",
            "couldn't've": "could not have",
            "didn't": "did not",
            "doesn't": "does not",
            "don't": "do not",
            "hadn't": "had not",
            "hadn't've": "had not have",
            "hasn't": "has not",
            "haven't": "have not",
            "he'd": "he would",
            "he'd've": "he would have",
            "he'll": "he will",
            "he'll've": "he will have",
            "he's": "he is",
            "how'd": "how did",
            "how'd'y": "how do you",
            "how'll": "how will",
            "how's": "how is",
            "I'd": "I would",
            "I'd've": "I would have",
            "I'll": "I will",
            "I'll've": "I will have",
            "I'm": "I am",
            "I've": "I have",
            "isn't": "is not",
            "it'd": "it had",
            "it'd've": "it would have",
            "it'll": "it will",
            "it'll've": "it will have",
            "it's": "it is",
            "let's": "let us",
            "ma'am": "madam",
            "mayn't": "may not",
            "might've": "might have",
            "mightn't": "might not",
            "mightn't've": "might not have",
            "must've": "must have",
            "mustn't": "must not",
            "mustn't've": "must not have",
            "needn't": "need not",
            "needn't've": "need not have",
            "o'clock": "of the clock",
            "oughtn't": "ought not",
            "oughtn't've": "ought not have",
            "shan't": "shall not",
            "sha'n't": "shall not",
            "shan't've": "shall not have",
            "she'd": "she would",
            "she'd've": "she would have",
            "she'll": "she will",
            "she'll've": "she will have",
            "she's": "she is",
            "should've": "should have",
            "shouldn't": "should not",
            "shouldn't've": "should not have",
            "so've": "so have",
            "so's": "so is",
            "that'd": "that would",
            "that'd've": "that would have",
            "that's": "that is",
            "there'd": "there had",
            "there'd've": "there would have",
            "there's": "there is",
            "they'd": "they would",
            "they'd've": "they would have",
            "they'll": "they will",
            "they'll've": "they will have",
            "they're": "they are",
            "they've": "they have",
            "to've": "to have",
            "wasn't": "was not",
            "we'd": "we had",
            "we'd've": "we would have",
            "we'll": "we will",
            "we'll've": "we will have",
            "we're": "we are",
            "we've": "we have",
            "weren't": "were not",
            "what'll": "what will",
            "what'll've": "what will have",
            "what're": "what are",
            "what's": "what is",
            "what've": "what have",
            "when's": "when is",
            "when've": "when have",
            "where'd": "where did",
            "where's": "where is",
            "where've": "where have",
            "who'll": "who will",
            "who'll've": "who will have",
            "who's": "who is",
            "who've": "who have",
            "why's": "why is",
            "why've": "why have",
            "will've": "will have",
            "won't": "will not",
            "won't've": "will not have",
            "would've": "would have",
            "wouldn't": "would not",
            "wouldn't've": "would not have",
            "y'all": "you all",
            "y'alls": "you alls",
            "y'all'd": "you all would",
            "y'all'd've": "you all would have",
            "y'all're": "you all are",
            "y'all've": "you all have",
            "you'd": "you had",
            "you'd've": "you would have",
            "you'll": "you you will",
            "you'll've": "you you will have",
            "you're": "you are",
            "you've": "you have"
            }
        c_re = re.compile('(%s)' % '|'.join(self.cList.keys()))
        return c_re
    def expandContractions(self,text):
        c_re = self.c_re
        def replace(match):
            return self.cList[match.group(0)]
        return c_re.sub(replace, text)

    def clean_tweets(self,tweets):
        cleaned_tweets = []
        for tweet in tweets:
            tweet = str(tweet)
            # if url links then dont append to avoid news articles
            # also check tweet length, save those > 10 (length of word "depression")
            if re.match("(\w+:\/\/\S+)", tweet) == None and len(tweet) > 10:
                #remove hashtag, @mention, emoji and image URLs
                tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|(\#[A-Za-z0-9]+)|(<Emoji:.*>)|(pic\.twitter\.com\/.*)", " ", tweet).split())
                
                #fix weirdly encoded texts
                tweet = ftfy.fix_text(tweet)
                
                #expand contraction
                tweet = self.expandContractions(tweet)

                #remove punctuation
                tweet = ' '.join(re.sub("([^0-9A-Za-z \t])", " ", tweet).split())

                #stop words
                stop_words = set(stopwords.words('english'))
                word_tokens = nltk.word_tokenize(tweet) 
                filtered_sentence = [w for w in word_tokens if not w in stop_words]
                tweet = ' '.join(filtered_sentence)

                #stemming words
                tweet = PorterStemmer().stem(tweet)
                
                cleaned_tweets.append(tweet)

        return cleaned_tweets
    
    def predict(self,tweet):
        test_arr = [tweet]
        sentiment = self.sentiment.polarity_scores(tweet)
        max_sent = max(sentiment)
        score_sent = 0
        if max_sent == 'pos':
            score_sent = 1-sentiment[max_sent]
        elif max_sent == 'neg':
            score_sent = sentiment[max_sent]
        else:
            score_sent = 0.5

        # X_t = self.clean_tweets(test_arr)
        X_t = test_arr
        # print(test_arr)
        sequences_t = self.tokenizer.texts_to_sequences(X_t)
        data_t = pad_sequences(sequences_t, maxlen=self.MAX_SEQUENCE_LENGTH)
        score = self.model.predict(data_t)
        print(score_sent, score)
        total_score = (2*score_sent+score)/3
        keras.backend.clear_session()
        return total_score



if __name__ == '__main__':
    model = TwitterModel()
    print(model.predict('i overthink a lot, im sensitive and clingy but i really do try my hardest to be good enough so im sorry if thats not enough.'))

'''
'I miss you. Wish you were right by my side and not with someone else #depressed since 2014'  0.9870599508285522
'Feeling happy but depressed'   0.8670069575309753
'Not feeling good'    0.0026930675376206636
'I miss you. Wish you were right by my side and not with someone else'   0.011307147331535816

'''