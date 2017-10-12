from collections import defaultdict
import csv
import re
import ronald_brain.constants as constants

emoticon_regex = r"""
    (?:
        [:=;]
        [oO\-]?
        [D\)\]\(\]/\\OpP]
    )""" # eyes, nose, mouth (in that order)

tweet_regexes = [
    emoticon_regex,
    r'(?:@[\w_]+)', # @ tag
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hashtag
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # url
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

token_reg = re.compile(r'('+'|'.join(tweet_regexes)+')', re.VERBOSE | re.IGNORECASE)



def tokenize_tweet(tweet):
    """
    Turn the tweet into a list of individual tokens. We will maintain hashtags, urls, etc., and not split them up
    Maybe add named-entity recognition?

    :param tweet:
    :return list of tokens:
    """
    toks = token_reg.findall(tweet)
    return [t.lower() for t in toks]

def word_n_grams(tokens, n):
    """
    This function simply splits the tokenized text into n-tuples representing n-grams.
    The * operator splits a list into a series of arguments passed to a function.

    So effectively, this function calls:
        return zip(tokens[1:], tokens[2:], ..., tokens[n:])

    This offsets the list by 1 for each successive argument, zipping words together in sequences of n

    :param tokens:
    :param n:
    :return a zip object (like a list) of n-tuples representing n-grams of the tokens:
    """
    if n == 1:
        return tokens

    return zip(*[tokens[i:] for i in range(n)])

def gen_word_seq_probabilities(ngrams):
    """
    Takes an iterable of n-tuples, which represents all the n-grams in a corpus, and returns the probability of the
    last item in the tuples following the previous sequence

    :param ngrams:
    :return a dict of dicts, mapping words to probability distributions of each word appearing after it:
    """

    prob_dist = defaultdict(list)
    for g in ngrams:
        # n-gram keys will be stored as comma-separated string values like "first,second"
        prob_dist[constants.WORD_KEY_DELIMITER.join(g[:-1])].append(g[-1])

    for word_seq in prob_dist.keys():
        next_words = prob_dist[word_seq]
        num_next_words = len(next_words)
        unq_next_words = set(next_words)

        # the probability of each word appearing after the word_seq
        next_word_prob_dist = {}

        for w in unq_next_words:
            next_word_prob_dist[w] = float(next_words.count(w)) / num_next_words
        prob_dist[word_seq] = next_word_prob_dist

    return prob_dist

def unigram_probs(filename):
    raw_tweets = process_csv(filename)
    tokenized_tweets = [tokenize_tweet(t) for t in raw_tweets]
    items = [token for full_tweet in tokenized_tweets for token in full_tweet]

    prob_dist = defaultdict(int)
    num_words = len(items)
    for i in items:
        if i in prob_dist:
            prob_dist[i] += 1
        else:
            prob_dist[i] = 1

    unq_items = set(items)

    for w in unq_items:
        prob_dist[w] = prob_dist[w] / num_words

    #print(prob_dist)
    return prob_dist

def process_csv(filename):
    """

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

def get_n_gram_probs(filename, n=2):
    """
    Given a filename and a value for N, this will return the probability districution for the n-grams associated with
    the tweets in the file. It is designed to work with a specific csv format at the moment.

    :param filename:
    :param n:
    :return probability distibution in the form of a dictionary of dictionaries:
    """
    raw_tweets = process_csv(filename)
    tokenized_tweets = [tokenize_tweet(t) for t in raw_tweets]
    total_tokens = [token for full_tweet in tokenized_tweets for token in full_tweet]

    ngrams = word_n_grams(total_tokens, n)

    prob_dist = gen_word_seq_probabilities(ngrams)

    return prob_dist