#This module takes user input to filter tweets by, then saves these filtered tweets into data.txt

#Import the necessary methods from tweepy library
import tweepy
import os
import json
import re

consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']
'''
To add environment variables
------------------------------------
For Windows:
control panel > system and security > system > advanced system settings > environment variables

For Mac:
add to .bash_profile in home directory
'''


#This is a basic listener that prints tweets and saves to raw_data.txt.
class listener(tweepy.StreamListener):

    def on_data(self, raw_data):
        with open('raw_data.txt','a') as thing:
            thing.write(raw_data)
        data = json.loads(raw_data)
        if 'RT' not in data['text'][0:3]:
	        with open('data.txt','a') as thing:
	        	try:
	        		thing.write(clean_tweet(data['extended_tweet']['full_text'])+'\n')
	        	except KeyError:
	        		thing.write(clean_tweet(data['text'])+'\n')
	        print(data['text'])
	        print('-----------------')
        return True

    def on_error(self, status):
        if status == '420':
            return False
        print(status)

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9_]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
    # first group takes out mentions 'ex: @Susan', second group takes out special characters, third group takes out links

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, listener()) #connects to twitter api

    #This captures input to filer tweets by
    filters = ['@realdonaldtrump']
    # while True:
    #     user_input = input('Enter a keyword to filter tweets by (Type EXIT to stop): ')
    #     if user_input == 'EXIT': break
    #     else: filters.append(user_input)
    stream.filter(track=filters)