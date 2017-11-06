import os.path
import csv
import numpy as np

import tweepy
from conf import twitter_credentials
from ronald_brain.util.constants import CSV_FILE_LOCATION

auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_KEY, twitter_credentials.ACCESS_SECRET)
api = tweepy.API(auth)


def load_csv(filename):
    """
    Select the column of the CSVs containing the tweet text and return them all as a list
    :param filename:
    :return a list of strings, where each string is a raw tweet:
    """
    raw_tweets = []

    with open(filename, newline='') as raw:
        next(raw)
        r = csv.reader(raw, delimiter=',')
        for row in r:
            raw_tweets.append(row[2])

    return raw_tweets

def get_tweets(user):
    file = ''.join((CSV_FILE_LOCATION, "%s_tweets.txt" % user))
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
        writer = csv.writer(f, delimiter=',')
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)

    return outtweets