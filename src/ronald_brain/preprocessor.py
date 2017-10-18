from collections import defaultdict
import csv
from enum import Enum
import nltk.data
import re
import ronald_brain.constants as constants
import sys

class Ngram(Enum):
    WORD = 1
    SENT_LENGTH = 2
    POS_TAG = 3

class Preprocessor:
    """
    This class should handle any pre-processing and model-creation required for text generation.
    It will read the raw data, convert it to the required formats, transform it into the metrics we will use
      and spit it out when asked
    """
    def __init__(self, filename):
        """
        Create the regex's required to tokenize the tweets
        TODO: a regex set for tokenizing Trump speeches, or other data sources?
        :param filename:
        """
        self._emoticon_regex = r"""
            (?:
                [:=;]
                [oO\-]?
                [D\)\]\(\]/\\OpP]
            )"""  # eyes, nose, mouth (in that order)

        self._tweet_regexes = [
            self._emoticon_regex,
            r'(?:@[\w_]+)',  # @ tag
            r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hashtag
            r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # url
            r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
            r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
            r'(?:[\w_]+)',  # other words
            r'(?:\S)'  # anything else
        ]
        self.token_reg = re.compile(r'(' + '|'.join(self._tweet_regexes) + ')', re.VERBOSE | re.IGNORECASE)
        self.raw_tweets = self.load_csv(filename)

    def tokenize_raw_data(self, raw_data):
        tokenized_tweets = [self.tokenize_tweet(t) for t in self.raw_tweets]

        return [token for full_tweet in tokenized_tweets for token in full_tweet]

    def split_into_sentences(self, raw_data):
        sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = [sentence.split() for t in raw_data for sentence in sentence_tokenizer.tokenize(t)]

        return [len(s) for s in sentences]

    def build_n_grams(self, items, n):
        """
            This function simply splits the items into n-tuples representing n-grams.
            The * operator splits a list into a series of arguments passed to a function.

            So effectively, this function calls:
                return zip(items[1:], items[2:], ..., items[n:])

            This offsets the list by 1 for each successive argument, zipping items together in sequences of n

            :param items:
            :param n:
            :return a zip object (like a list) of n-tuples representing n-grams of the tokens:
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

    def tokenize_tweet(self, tweet):
        """
            Turn the tweet into a list of individual tokens. We will maintain hashtags, urls, etc., and not split them up
            Maybe add named-entity recognition?

            :param tweet:
            :return list of tokens:
            """
        toks = self.token_reg.findall(tweet)
        return [t.lower() for t in toks]

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

    def build_ngram_probability_model(self, ngrams, n):
        """
        Takes an iterable of n-tuples, and - for each of those tuples - returns the probability of the
        last item in the tuple following the previous sequence of items

        This will work with any input of tuples composed of strings, i.e.:
        [("4", "3", "2"), ("3", "3", "1"), ..., ("5", "1", "2")] # For sentence lengths
        [("the", "quick", "brown"), ("quick", "brown", "fox"), ..., ("the", "lazy", "fox")] # for words

        :param ngrams:
        :return a dict of dicts, mapping words to probability distributions of each word appearing after it:
        """

        if n == 1:
            # Handle the unigram case
            # (Maybe this can be handled in the general algorithm)
            prob_dist = defaultdict(int)
            num_words = len(ngrams)
            for i in ngrams:
                key = i[0]
                if key in prob_dist:
                    prob_dist[key] += 1
                else:
                    prob_dist[key] = 1

            unq_items = [str(i) for i in set(ngrams)]

            for k in unq_items:
                prob_dist[k] = prob_dist[k] / num_words

            return prob_dist
        else:
            prob_dist = defaultdict(list)

            for g in ngrams:
                # n-gram keys will be stored as strings separated by KEY_DELIMITER
                prob_dist[constants.KEY_DELIMITER.join(g[:-1])].append(g[-1])

            for seq in prob_dist.keys():
                possible_next = prob_dist[seq]
                num_next = len(possible_next)
                unq_next = set(possible_next)

                # the probability of each word appearing after the word_seq
                next_prob_dist = {}

                for t in unq_next:
                    next_prob_dist[t] = float(possible_next.count(t)) / num_next
                prob_dist[seq] = next_prob_dist


            return prob_dist

    def ngram_probabilities(self, type, n):
        """
        This is where we differentiate between the Ngram types.
        Add a new branch in the if/else tree for a new Ngram type
        :param type:
        :param n:
        :return the probability distribution for n-grams of type `type` and order `n`:
        """
        if type == Ngram.WORD:
            print("Building WORD %s-grams..." % (n))
            ngrams = self.build_n_grams(self.tokenize_raw_data(self.raw_tweets), n)
            print("WORD %s-grams built!" % (n))

            print("Building WORD %s-gram prob-dist..." % (n))
            prob_dist = self.build_ngram_probability_model(ngrams, n)
            print("%s-gram WORD prob-dist built" % (n))

            return prob_dist
        elif type == Ngram.SENT_LENGTH:
            print("Building SENT-LEN %s-grams..." % (n))
            ngrams = self.build_n_grams(self.split_into_sentences(self.raw_tweets), n)
            print("SENT-LEN %s-grams built!" % (n))

            print("Building SENT-LEN %s-gram prob-dist..." % (n))
            prob_dist = self.build_ngram_probability_model(ngrams, n)
            print("%s-gram SENT-LEN prob-dist built" % (n))
            return prob_dist

    def build_ngram_model_list(self, n, type):
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
            return [self.ngram_probabilities(type, n)]
        elif n > 1:
            m = self.ngram_probabilities(type, n)
            return self.build_ngram_model_list(n - 1, type) + [m]
