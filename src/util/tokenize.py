import nltk
from .constants import NON_ENGLISH_WORDS, TWEET_REGEXES
import enchant
import re
from nltk.corpus import stopwords

token_reg = re.compile(r'(' + '|'.join(TWEET_REGEXES) + ')', re.VERBOSE | re.IGNORECASE)
d = enchant.Dict("en_UK")

def get_flat_tokens(tokenized_tweets):
    '''
    Flatten a list of lists into a single list
    :param tokenized_tweets:
    :return:
    '''
    return [token for tweet in tokenized_tweets for token in tweet]

def remove_stops(tokens):
    stop_words = list(stopwords.words('english'))
    return [t for t in tokens if t not in stop_words]



def tokenize_raw_tweets(raw_tweets):
    '''
    Turn the raw data into a list of lists of tokens

    :param raw_data:
    :return:
    '''
    tokenized_tweets = [tokenize_tweet(t) for t in raw_tweets]
    return tokenized_tweets


def tokenize_tweet(tweet):
    """
    Turn the tweet into a list of individual tokens. We will maintain hashtags, urls, etc., and not split them up
    Maybe add named-entity recognition?

    :param tweet:
    :param token_reg:
    :return list of tokens:
    """
    # print(type(tweet))
    # print(tweet)
    toks = token_reg.findall(tweet)
    return [t.lower() for t in toks]


def split_into_sentences(raw_data):
    '''
    The data is a list of tweet strings. Each of these tweets will be split into sentences

    :param raw_data:
    :return a list of lists, each outer list is a tweet and each inner list is a sentence in the tweet:
    '''
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    split_sentences = [sentence_tokenizer.tokenize(tweet) for tweet in raw_data]

    return split_sentences


def words_only(total_tokens):
    '''
    Filter the tokens to remove tokens which are not English words
    :param total_tokens:
    :return:
    '''
    words = [w for w in total_tokens if w not in NON_ENGLISH_WORDS]

    words = [w for w in words if d.check(w)]


    return words