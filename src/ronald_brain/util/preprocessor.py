import csv
import re
import sys
from enum import Enum
from .twitter import tweets

import nltk.data
from nltk.corpus import stopwords
import enchant

from ronald_brain.models.markov_chain import MarkovChain
from .constants import TWEET_REGEXES, FRONT_PUNCTUATION, USELESS_PUNCTUATION, NON_ENGLISH_WORDS


class Ngram(Enum):
    WORD = 1
    SENT_LENGTH = 2
    POS_TAG = 3
    FIRST_WORD = 4

class Preprocessor:
    """
    This class should handle any pre-processing and model-creation required for text generation.
    It will read the raw data, convert it to the required formats, transform it into the metrics we will use
      and spit it out when asked
    """
    def __init__(self, user):
        """
        Create the regex's required to tokenize the tweets
        TODO: a regex set for tokenizing Trump speeches, or other data sources?
        :param filename:
        """
        self._tweet_regexes = TWEET_REGEXES
        self.token_reg = re.compile(r'(' + '|'.join(self._tweet_regexes) + ')', re.VERBOSE | re.IGNORECASE)

        ### Keep the raw_tweets to be re-used as needed
        self.raw_tweets = tweets.get_tweets(user)
        self.raw_tweets = [t[2] for t in self.raw_tweets]
        self.tokenized_total = self.tokenize_raw_data(self.raw_tweets)


    ###############################
    ####     LOADING DATA      ####
    ###############################

    def load_csv(self, filename):
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

    def tweets_as_string(self):
        return ''.join(self.raw_tweets)


    ###############################
    ####    TOKENIZING DATA    ####
    ###############################

    def tokenize_raw_data(self, raw_data):
        '''
        Turn the raw data into a single list of tokens

        :param raw_data:
        :return:
        '''
        tokenized_tweets = [self.tokenize_tweet(t) for t in self.raw_tweets]

        return [token for full_tweet in tokenized_tweets for token in full_tweet]

    def tokenize_tweet(self, tweet):
        """
        Turn the tweet into a list of individual tokens. We will maintain hashtags, urls, etc., and not split them up
        Maybe add named-entity recognition?

        :param tweet:
        :return list of tokens:
        """
        toks = self.token_reg.findall(tweet)
        return [t.lower() for t in toks]

    def split_into_sentences(self, raw_data):
        '''
        The data is a list of tweet strings. Each of these tweets will be split into sentences

        :param raw_data:
        :return a list of lists, each outer list is a tweet and each inner list is a sentence in the tweet:
        '''
        sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        split_sentences = [sentence_tokenizer.tokenize(tweet) for tweet in raw_data]

        return split_sentences

    def words_only(self):
        stop = set(stopwords.words('english') + FRONT_PUNCTUATION + USELESS_PUNCTUATION + NON_ENGLISH_WORDS)

        words = [w for w in self.tokenized_total if not w in stop]
        d = enchant.Dict("en_UK")

        words = [w for w in words if d.check(w)]

        return words




        ###############################
        ####    BUILDING NGRAMS    ####
        ###############################

    def first_words_unigram(self, raw_data, n):
        '''
        Gets the first n words of each sentence and returns it as a unigram
        Returns something like:
                ["we must", "Jeb is"] if n == 2
                        or
                ["we must make", "Jeb is a"] if n == 3

        :param raw_data:
        :param n:
        :return list of strings, where each string contains `n` words:
        '''
        tweets = self.split_into_sentences(raw_data)
        tokenized_sentences = [self.tokenize_tweet(sentence) for tweet in tweets for sentence in tweet]
        first_words = [tuple(s[:n]) for s in tokenized_sentences]

        return first_words

    def build_n_grams(self, items, n):
        """
        This function simply splits the items into n-tuples representing n-grams.
        The * operator splits a list into a series of arguments passed to a function.

        So effectively, this function calls:
            return zip(items[1:], items[2:], ..., items[n:])

        This offsets the list by 1 for each successive argument, zipping items together in sequences of n

        :param items:
        :param n:
        :return a list of n-tuples representing n-grams of the tokens:
        """

        if n == 1:
            # ngrams will be tuples of strings, regardless of data being ints or strings
            # i.e. [ ("12",), ("2",), ("8",) ] is an example of a unigram list for sentence length
            foo = [(str(i),) for i in items]
            return foo

        raw_ngrams = zip(*[items[i:] for i in range(n)])
        string_ngrams = [self.tup_to_string(t) for t in raw_ngrams]
        return string_ngrams

    def tup_to_string(self, tup):
        """
        Convert each of the items of a tuple into strings and return the tuple
        :param tup:
        :return:
        """
        return tuple(str(s) for s in tup)



    ###############################
    ####  BUILD MARKOV CHAINS  ####
    ###############################

    def build_markov_chain(self, type, n):
        """
        This is where we differentiate between the Ngram types.
        Add a new branch in the if/else tree for a new Ngram type
        :param type:
        :param n:
        :return the probability distribution for n-grams of type `type` and order `n`:
        """
        if type == Ngram.WORD:
            ngrams = self.build_n_grams(self.tokenized_total, n)

            markov_chain = MarkovChain(ngrams, n)

            return markov_chain
        elif type == Ngram.SENT_LENGTH:
            sentence_tweets = self.split_into_sentences(self.raw_tweets)
            split_sentences = [sentence.split() for sentences in sentence_tweets for sentence in sentences]
            ngrams = self.build_n_grams([len(s) for s in split_sentences], n)

            markov_chain = MarkovChain(ngrams, n)

            return markov_chain
        elif type == Ngram.FIRST_WORD:
            first_words_ngrams = self.first_words_unigram(self.raw_tweets, n)

            markov_chain = MarkovChain(first_words_ngrams, 1) # Starting words is always treated like a unigram case

            return markov_chain

    def build_model_list(self, n, type):
        """
        Recursively build a list of models for n > 2.
        We want a list of models so that we can implement the Backoff algorithm
        https://www.quora.com/What-is-backoff-in-NLP

        :param models:
        :return a list of n-gram models:
        """
        if (n < 1):
            print("N must be at least 1. Quitting.")
            # TODO: Exception
            sys.exit(0)
        elif n == 1:
            return [self.build_markov_chain(type, n)]
        elif n > 1:
            m = self.build_markov_chain(type, n)
            return self.build_model_list(n - 1, type) + [m]
