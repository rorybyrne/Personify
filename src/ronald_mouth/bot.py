import tweepy
from ronald_brain import generator
#import twitter_credentials

auth = tweepy.OAuthHandler('b9nh8obvDFh7YYIKpHrLJ9a2T', '37lhcaIiGie8bA9h1bS0ajxs0eYfB7NFJ3hfUltWhVR9MJTpRt')
auth.set_access_token('918405736127979521-C5JxvHj24tYgKcB6CFTBdrHCO80JMd4', 'PbMvexD7WXrKMMU7cI1U8605ynlCurcBUnam5hBzvX3Yg')
api = tweepy.API(auth)

def send_tweet(text):

    return api.update_status(text)
