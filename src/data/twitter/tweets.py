import argparse
import csv
import os.path
from os.path import dirname
import sys

root_path = dirname(dirname(dirname(__file__)))
# Add the root to the path so that import work correctly
sys.path.append(root_path)

import tweepy

from conf import get_credentials
from util.constants import TWEET_LOC_REAL
from util import log

logger = log.logger

logger.info("Adding %s to the path" % root_path)



def parse_args():
    '''
        Basic argument parser. Additions here need to be reflected in
        config.settings also.
    '''
    parser = argparse.ArgumentParser(description='''Cluster and Visualise Text Data''')
    parser.add_argument('--user',
                        help="Twitter username whose Tweets we will download",
                        type=str,
                        default="realdonaldtrump",
                        metavar="USER")

    return parser.parse_args()

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
    file = ''.join((TWEET_LOC_REAL, "%s_tweets.csv" % user))
    logger.info("Loading tweets for %s from %s" % (user, file))
    if (not os.path.exists(file)):
        logger.info("Tweets for %s not found in filesystem. Will download first")
        download_tweets(user)

    return load_csv(file)

def download_tweets(user):
    creds = get_credentials.get_credentials(user)

    auth = tweepy.OAuthHandler(creds["c_key"], creds["c_secret"])
    auth.set_access_token(creds["a_key"], creds["a_secret"])
    api = tweepy.API(auth)

    file = ''.join((TWEET_LOC_REAL, "%s_tweets.csv" % user))
    logger.info("Downloading %s tweets to %s" % (user, file))
    if (os.path.exists(file)):
        raise FileExistsError("We already have Tweets for %s" % user)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=user, count=200, tweet_mode="extended")
    for t in new_tweets:
        print(t.full_text)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        logger.debug("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=user, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        logger.debug("...%s tweets downloaded so far" % (len(alltweets)))

    outtweets = [[tweet.id_str, tweet.created_at, tweet.full_text] for tweet in alltweets]
    logger.debug("\n%s total tweets" % len(outtweets))

    with open(file, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='~')
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)

if __name__ == '__main__':
    opts = parse_args()
    download_tweets(opts.user)