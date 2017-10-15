import tweepy
from ronald_brain import generator
#import twitter_credentials

auth = tweepy.OAuthHandler(XXXX, XXXX)
auth.set_access_token(XXXX, XXXX)
api = tweepy.API(auth)

def send_tweet(text):

    return api.update_status(text)
