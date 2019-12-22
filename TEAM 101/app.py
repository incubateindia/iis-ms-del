# from datetime import datetime
import os
import time
from flask import Flask, request, jsonify, json 

import subprocess
import sys

from Recent_tweets import *
from getTwitterID import *
from audio_prediction import audio_predict
from current_photo_model import *
from Instagram_model import *
from twitter_model import *
from photo_uploads.downloadImage import *
from mood_recommend import *
from typemachineProcess import *


app = Flask(__name__)

app.config['AUDIO_UPLOADS']="./audio_uploads/"
app.config['PHOTO_UPLOADS']="./photo_uploads/"
LASTtime = '2019-10-12 07:15:18'

# MODEL initiations

photo_model = EmotionNet()
inta_model = EmotionNet()

class User():
	def __init__(self, name, twitter_username):
		self.name = name
		self.twitter_username = twitter_username


class Post():
	def __init__(self, name, twitter_username):
		self.name = name
		self.twitter_username = twitter_username

@app.route('/adduser',methods=['GET','POST'])
def adduser():
    if request.method=='POST':
        user_json = request.get_json()
        user = User(name=user_json['name'], twitter_username=user_json['twitter_username'])
        print(user.name)
        return 'Successful'
    return "dkjhakjh"

@app.route('/getTwitter/<date>',methods = ['POST'])
def getTwitter(date):
    if request.method=='POST':
        post_json = request.get_json()
        twitter_username = post_json['twitter_username']
        # return "success"
        tweets = getTimedTweets(twitter_username,date)
        output=[]
      
        for t in tweets:
            print(t[0])
            twitter_model = TwitterModel()
            result = twitter_model.predict(str(t[0]))
            result = str(int(1+4*result+0.75))
            t.append(result)
            output.append(t)
        return jsonify(output)

    return 'waiting'

@app.route('/audio', methods=['POST'])
def upload_audio():
    if request.method=='POST':
        if request.files:
            file = request.files['file']
            if file.filename=='':
                return "empty"
            if file: 
                filename = file.filename
                file.save(os.path.join(app.config['AUDIO_UPLOADS'],filename))
                print(filename)
                # return "successful"
                result = audio_predict("./audio_uploads/"+filename)
                return str(result)
    return "waiting"

@app.route('/currentPhoto', methods=['POST'])
def upload_photo():
    if request.method=='POST':
        print("got photo")
        print(request)
        if request.files:
            file = request.files['file']
            print(file)
            if file.filename=='':
                return "empty"
            if file: 
                filename = file.filename
                file.save(os.path.join(app.config['PHOTO_UPLOADS'],filename))
                print(filename)
                
                print('Testing Image')
                result,score = photo_model.predict('./photo_uploads/'+filename)
                
                print(result)
                return str(score)
                # return "successful"
    return "waiting"

@app.route('/instaArray', methods=['POST'])
def upload_insta_array():
    if request.method=='POST':
        print("got photo")
        print(request)
        # post_json = request.get_data()
        post_json = request.get_json()
        # for i in range(len(post_json)) :
        #     print(post_json[i])
        # print(post_json[0][0])
        
        output = []
        for i in range(len(post_json)) :
            
            img_url = post_json[i][0]
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(post_json[i][1])))
            insta_filename = str(date)
            saveimg(img_url,insta_filename)
            print('Testing Image', insta_filename)
            insta_model = EmotionNet()
            result,score = insta_model.predict(insta_filename+'.jpg')
            print(result)
            # return str(score)
            t = [str(score),str(post_json[i][1]),str(date),str(img_url)]
            # t.append(str(score))
            # t.append(str(post_json[i][1])
            # t.append(str(date))
            # t.append(str(img_url))
            output.append(t)
        return jsonify(output)
        
        # return "successful"
    return "waiting"
    
@app.route('/insta/<date_epoch>', methods=['POST'])
def upload_insta(date_epoch):
    if request.method=='POST':
        print("got photo")
        print(request)
        post_json = request.get_json()
        img_url = post_json['img_url']
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(date_epoch)))
        insta_filename = str(date)
        saveimg(img_url,insta_filename)
        print('Testing Image', insta_filename)
        insta_model = InstaNet()
        result,score = insta_model.predict(insta_filename+'.jpg')
        print(result)
        # return str(score)
        return jsonify(
            {
                "score":str(score),
                "date_epoch": str(date_epoch),
                "date":str(date),
                "url":img_url
            }
        )
        # return "successful"
    return "waiting"
# @app.route('/getStats/<user_id>')
# def get_stats(name):
#     post = Post.query.filter_by(user_id=user_id)
#     return jsonify(
#             {
#                 # "id":post.id,
#                 "user_id":post.user_id,
#                 "platform":str(post.platform),
#                 "caption":post.caption,
#                 "text":post.text,
#                 "isImg":post.isImg,
#                 "ImgURL":post.ImgURL,
#                 "isAudio":post.isAudio,
#                 "AudioName":post.AudioName,
#                 "time_created":post.time_created,
#                 "result":post.result
#             }
#         )n 
@app.route('/typemachine', methods=['POST'])
def typemachine():
    if request.method=='POST':
        print("typemachine")
        print(request)
        post_json = str(request.get_data())
        print(post_json)
        result = []
        result.append(getFlags(post_json))
        return jsonify(result)

@app.route('/recommend/<score>', methods=['POST'])
def recommend(score):
    rec = RecommendEmotion(str(score))
    movies = rec.movies()
    blogs = rec.blogs()
    books = rec.books()
    songs = rec.songs()

    rec_ = jsonify({
        "movies":movies,
        "blogs":blogs,
        "books":books,
        "songs":songs
    })
    return rec_
    # movie_json = []
    # for m in movies:
    #     x = jsonify(m)
    #     # for p in m:
    #     #     x = jsonify({
    #     #         'name':p[0],
    #     #         'url':p[1],
    #     #         'img_url':p[2]
    #     #     })
    #     movie_json.append(x)
    # return jsonify(movie_json)

if __name__ == '__main__':
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tweepy 3.8.0"])
    app.run(debug=True, host='0.0.0.0', port=5000)
    # app.run()