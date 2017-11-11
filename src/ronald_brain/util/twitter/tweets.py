import os.path
import csv
import numpy as np

import tweepy
from conf import get_credentials
from ronald_brain.util.constants import CSV_FILE_LOCATION



def load_csv(filename):
    """
    Select the column of the CSVs containing the tweet text and return them all as a list
    :param filename:
    :return a list of strings, where each string is a raw tweet:
    """
    raw_tweets = []

    with open(filename, newline='') as raw:
        next(raw)
        r = csv.reader(raw, delimiter='~')
        for row in r:
            raw_tweets.append(row)

    return raw_tweets

def get_tweets(user):
    print("Getting tweets for user %s" % user)
    creds = get_credentials.get_credentials(user)

    auth = tweepy.OAuthHandler(creds["c_key"], creds["c_secret"])
    auth.set_access_token(creds["a_key"], creds["a_secret"])
    api = tweepy.API(auth)

    file = ''.join((CSV_FILE_LOCATION, "%s_tweets.csv" % user))
    if(os.path.exists(file)):
        return load_csv(file)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=user, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=user, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    print("\n%s total tweets" % len(outtweets))

    with open(file, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='~')
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)

    return outtweets