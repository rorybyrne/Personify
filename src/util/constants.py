import logging

#######################
### PROJECT DETAILS ###
#######################

PROJECT_NAME = "Personify"
LOG_LEVEL = logging.DEBUG

#######################
### TWITTER DETAILS ###
#######################

TWITTER_ACCOUNTS = {
    "DONALD_TRUMP" : "realdonaldtrump",
    "MARK_HUMPHRYS": "markhumphrys"
}

TWEET_LOC_REAL = 'data/real/'

########################
### MODEL PARAMETERS ###
########################

KEY_DELIMITER = ' '
CONSTANT = 5
START_TOKEN = '<START>'
FIRST_WORDS_N = 1

SENTENCE_LENGTH_COEF = 0.6

MAX_OVERLAP_RATIO = 0.9
MAX_OVERLAP_TOTAL = 15

WEIGHTED_SENTENCE_ENDERS = {'.': 0.8,
                            '!': 0.1,
                            '?': 0.1}

###########
### NLP ###
###########

FRONT_PUNCTUATION = [',', '.', '?', '!', ':', ';']
USELESS_PUNCTUATION = ['(', ')', '"', '\'', '^', '@', '-', '_', '*', '&', '$', '+', '=']
NON_ENGLISH_WORDS = ['rt', 'amp', 'Rt']

SENTENCE_ENDERS = ['.', '!', '?']


NUMBER_TWITTER_HANDLE_REGEX = r'\@*\w*\d+'



EMOTICON_REGEX= r"""
            (?:
                [:=;]
                [oO\-]?
                [D\)\]\(\]/\\OpP]
            )"""  # eyes, nose, mouth (in that order)

TWEET_REGEXES = [
    EMOTICON_REGEX,
    r'(?:@[\w_]+)',  # @ tag
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hashtag
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # url
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]