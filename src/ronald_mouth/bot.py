import tweepy
from conf import get_credentials

def send_tweet(text, user):
    creds = get_credentials.get_credentials(user)

    auth = tweepy.OAuthHandler(creds["c_key"], creds["c_secret"])
    auth.set_access_token(creds["a_key"], creds["a_secret"])
    api = tweepy.API(auth)

    return api.update_status(text)
