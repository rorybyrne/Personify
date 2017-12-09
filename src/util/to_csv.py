import argparse
import csv
from os.path import dirname
import sys

root_path = dirname(dirname(__file__))
# Add the root to the path so that import work correctly
sys.path.append(root_path)

from generate.markov_generator import MarkovGenerator
from util import log

logger = log.logger

logger.info("Adding %s to the path" % root_path)


def parse_args():
    '''
        Basic argument parser. Additions here need to be reflected in
        config.settings also.
    '''
    parser = argparse.ArgumentParser(description='''Produce a number of tweets based on a Twitter user, and then
                                                        write them to a csv file''')
    parser.add_argument('--user',
                        help="Twitter user whose Tweets we will copy",
                        type=str,
                        default="realdonaldtrump",
                        metavar="USER")
    parser.add_argument('--num-tweets',
                        help="The number of Tweets to produce",
                        type=int,
                        default=3000,
                        metavar="NUM_TWEETS")
    parser.add_argument('--output-dir',
                        help="Directory to save the Tweets",
                        type=str,
                        default="data/fake",
                        metavar="DIR")

    return parser.parse_args()

def write_tweets(user, num_tweets, file, delim):
    logger.info("Writing tweets to file %s" % file)
    with open(file, 'a', newline='') as f:
        w = csv.writer(f, delimiter=delim)
        w.writerow(['id', 'created_at', 'text'])

    gen = MarkovGenerator(user)
    for x in range(num_tweets):
        logger.info("Tweet #%s" % str(x+1))
        tweet = gen.generate(140)
        write_tweet(file, tweet, delim)


def write_tweet(file, tweet, delim):
    logger.info("Writing out tweet: %s" % tweet)
    with open(file, 'a') as f:
        w = csv.writer(f, delimiter=delim)
        w.writerow(['0', "2017-11-09 23:39:56", tweet])


if __name__ == '__main__':
    opts = parse_args()
    logger.info("Generating CSV of %s Tweets based on %s" % (opts.num_tweets, opts.user))
    file = opts.output_dir + "/" + opts.user + "_tweets.csv"
    write_tweets(opts.user, opts.num_tweets, file, "~")


