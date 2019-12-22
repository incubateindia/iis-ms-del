## GENERAL KEYWORD EXTRACTION KAFKA DUMP


## import necessary libraries
import tweepy ## for tweets extraction
from tweepy import Stream ## to handle the stream
from tweepy.streaming import StreamListener
import json
# from RAKE import Rake
# import spacy
# import nltk

from getTwitterID import getID

# from selenium import webdriver

# from datetime import datetime
# from datetime import timedelta



import unicodedata
import re

## remove accented chars
def rem_accent(text):
    text  = ''.join(c for c in unicodedata.normalize('NFD',text) if unicodedata.category(c) != 'Mn')
    return text

## remove hash and preserve information
def rem_hash(text):
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
    return text

## remove special characters
def rem_special(text):
    pattern = r'[^a-zA-Z0-9\s]'
    text = re.sub(pattern,'',text) ## match pattren in text and replace by ''
    return text

## correcting repeating characters
def rem_white(text):
    text = text.strip()
    return text 

def rem_url(text):
    text =  re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',text) 
    return text


## a class which will handle everything
class Extract(StreamListener): ## inherit Stream Listner to make custom streams of data
    def __init__(self):
        """ 
        Function to set up architecture for core functionality
        """
        self.CONSUMER_KEY = 'ivXoCzbsproSiZxXjclnxB2Ix'
        self.CONSUMER_SECRET = 't8NNlTvlWZ8KxzCALVKh1e1P8LCDAO0eRl6bPyiULoofQ9TqNc'
        self.OAUTH_TOKEN = '1131114814770745344-ypIJJd5aYzZSjf8bxdy3f26TLEWclO'
        self.OAUTH_TOKEN_SECRET = 'vP3Oh8UWildlAQGWSMOn30lBvmbGZQ3foDkugXEaBY6Ll'

        ## authorisation setup
        auth = tweepy.OAuthHandler(self.CONSUMER_KEY,self.CONSUMER_SECRET)
        auth.set_access_token(self.OAUTH_TOKEN,self.OAUTH_TOKEN_SECRET)
        api = tweepy.API(auth)
        self.api = api 
        self.auth = auth


        # self.affected_loc = ['Bihar', 'Punjab', 'Kerala', 'kerala' ,'Gujarat','Porbandar','Rajasthan','Delhi','New Delhi','Port Mundra','Gurgaon','Dharuhera','Jaipur','Ajmer','Udaipur','Rajkot','Morbi','India'] ## Place of our supply chain interest
        # self.watch_list = {} ## to keep track of locations that are still affected
        # self.loc_keyword = {} ## database of {loc:{keyword1:vol1,})
        # self.driver = webdriver.Chrome(executable_path='/home/ruchit/Downloads/chromedriver')


    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
    

    # def construct_url(self,keyword):
    #     today  = datetime.now()
    #     delta =  timedelta(days=2)
    #     until = str((today-delta).date())
        
    #     key_list = keyword.split() ## split by space
    #     url = 'https://twitter.com/search?q='
    #     url += '%20'.join(key_list)
    #     url += r'%20since%3A'+until
    #     url += r'%20&src=typd'
    #     print(url)
    #     return url


    # def get_volume(self,query):
    #     url = self.construct_url(query) ## get the url
    #     self.driver.get(url)
    #     ol = self.driver.find_element_by_class_name('stream-items')
    #     li = ol.find_elements_by_tag_name("li")
    #     return len(li)


    # def get_event(self,keyword_list,curr_locs):

    #     for loc in curr_locs:
    #         for word in keyword_list:
    #             query = word + ' ' + loc ## form the query
    #             vol = self.get_volume(query)
    #             ## now check if this event passes the threshold
    #             print('Word: {} , Vol: {}'.format(word,vol))
    #             if vol > 40:
    #                 if loc not in self.loc_keyword.keys():
    #                     self.loc_keyword[loc] = []
    #                 self.loc_keyword[loc].append(word) ## append the keyword
    #                 print('Event added ',word,vol)
        
    #     print('====================================')
    #     print('Location Event Pairs: ',self.loc_keyword)
    #     print('====================================')



    # def get_keywords(self,tweet,loc):
    #     ## extract the keywords 
    #     rake = Rake(min_length=1, max_length=2)
    #     print('Current Keywords for {}'.format(loc))
    #     ## extract the keywords out of our new tweet
    #     rake.extract_keywords_from_text(tweet)
    #     keyword_list = rake.get_ranked_phrases() ## a list of keywords by this tweet ;
    #     print('Got New Keywords: {}'.format(keyword_list)) ## new list of keywords
    #     ## take the top 3 keywords and append them to our list

    #     self.get_event(keyword_list,loc)

    # def get_location(self,tweet,user):
    #     """
    #     Extracts Location out of a tweet and Updates the watch list
    #     """
    #     print('Text: {}  and user: {}'.format(tweet,user))
    #     curr_locs = [] ## a list of current location 
    #     nlp = spacy.load('en') ## load in nlp pipes
    #     doc = nlp(tweet) ## create a doc model
    #     for words in doc.ents:
    #         if words.label_ == 'GPE' and words.text in self.affected_loc:
    #             if words.text not in self.watch_list.keys(): ## check if this location is already in the watch list
    #                 print("Alert {} affected".format(words.text))
    #                 self.watch_list[words.text] = [] ## init the tweet list
    #                 self.watch_list[words.text].append(tweet) ## store the tweet with loc as key
    #             else:
    #                 ## if already present then simply append the list
    #                 self.watch_list[words.text].append(tweet)
    #             curr_locs.append(words.text)
    #         else:
    #                 print(words.text ,' || ', words.label_)

    #     ## after updating the watch list , get the keywords on given set of location-tweet pair  
        # print('Watch List contains: ', self.watch_list)          
        # self.get_keywords(tweet,curr_locs) ## update keywords for these locations as changes will be made in them only
        # print('============================================================')
       

    def process(self,tweet):
        print(tweet)
        user = tweet['user']['screen_name'] 
        duplicate = user not in ['MirrorNow','jarvvvis' ,'ANI' , 'IndiaToday']
        if tweet['text'][:2] == 'RT' or  duplicate:
            return
        ## only original tweet

        ## do analysiz on this!!
        
        ## catch full text
        self.text = tweet['text']
        print(self.text)
        # self.get_location(rem_hash(rem_url(self.text)),tweet['user']['screen_name'])

        


    def on_data(self,data):
        try:
            tweet = json.loads(data)
            self.process(tweet)
        except KeyError as e:
            print(str(e))
        

    def on_error(self, status):
        print(status)
    

def stream_general(username):
    extract = Extract()
    stream = Stream(extract.auth,extract,timeout=30.0)
    ## ANI,IndiaToday,MirrorNow,weatherIndia
    # username = input()
    twitterID = getID(username)
    print(twitterID)
    stream.filter(follow=[twitterID]) 
    # '355989081','19897138','3638215945','920364181488132096','1018469286707367936',
    # media_url_https for photos



if __name__ == '__main__':
    username = input()
    stream_general(username)