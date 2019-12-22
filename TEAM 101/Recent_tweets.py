import tweepy 
from datetime import datetime


consumer_key = "ivXoCzbsproSiZxXjclnxB2Ix"
consumer_secret = "t8NNlTvlWZ8KxzCALVKh1e1P8LCDAO0eRl6bPyiULoofQ9TqNc"
access_key = "1131114814770745344-ypIJJd5aYzZSjf8bxdy3f26TLEWclO"
access_secret = "vP3Oh8UWildlAQGWSMOn30lBvmbGZQ3foDkugXEaBY6Ll"

# Function to extract tweets 
def get_tweets(username): 
		print(username)
		# Authorization to consumer key and consumer secret 
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

		# Access to user's access key and access secret 
		auth.set_access_token(access_key, access_secret) 

		# Calling api 
		api = tweepy.API(auth) 

		# 200 tweets to be extracted 
		# number_of_tweets=5
		tweets = api.user_timeline(screen_name=username) 

		# Empty Array 
		tmp=[] 

		# create array of tweet information: username, 
		# tweet id, date/time, text 
		# tweets_for_csv = [tweet.text and tweet.created_at for tweet in tweets] # CSV file created 
		for tweet in tweets: 

			# Appending tweets to the empty array tmp 
			tmp.append(
                        [
                            tweet.text,
                            str(tweet.created_at)
                        ]
                        ) 

		# Printing the tweets 
		return tmp

def getTimedTweets(username,date):
	print(username)
	tmp = get_tweets(username)
	# return tmp
	# return "adaj"
	output=[]
	for t in tmp:
		# print(t[1])
		# d = datetime.datetime(t[1]).timestamp()
		if t[1]>date:
			output.append(t)
		else:
			break
	return output
	# print(output)
# Driver code 
if __name__ == '__main__': 

	# Here goes the twitter handle for the user 
	# whose tweets are to be extracted. 
	# print(datetime.datetime(2012-10-12 07:15:18).timestamp())
	getTimedTweets("twitter-handle",'2012-10-12 07:15:18') 
