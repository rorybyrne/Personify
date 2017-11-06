import re
import sys
from enum import Enum
from .twitter import tweets

from .tokenize import *

from ronald_brain.models.markov_chain import MarkovChain


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
        Preprocesses and stores data for a twitter user
        :param user:
        """

        ### Keep the raw_tweets to be re-used as needed
        self.raw_tweets = tweets.get_tweets(user)

        self.tokenized_tweets = tokenize_raw_tweets(self.raw_tweets)
        self.tokenized_flat = get_flat_tokens(self.tokenized_tweets)

        self.words_only_flat = words_only(self.tokenized_flat)

        # Set this based on what kind of output you want
        # Should be a flat list of tokens
        self.tokens_to_use = self.words_only_flat

    def all_tweets_as_string(self):
        return ''.join(self.raw_tweets)


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
        tweets = split_into_sentences(raw_data)
        tokenized_sentences = [tokenize_tweet(sentence) for tweet in tweets for sentence in tweet]
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
            ngrams = self.build_n_grams(self.tokens_to_use, n)

            markov_chain = MarkovChain(ngrams, n)

            return markov_chain
        elif type == Ngram.SENT_LENGTH:
            sentence_tweets = split_into_sentences(self.raw_tweets)
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
