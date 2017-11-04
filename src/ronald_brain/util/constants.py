KEY_DELIMITER = ' '
CONSTANT = 5
START_TOKEN = '<START>'
FIRST_WORDS_N = 1

FRONT_PUNCTUATION = [',', '.', '?', '!', ':', ';']
USELESS_PUNCTUATION = ['(', ')', '"', '\'', '^', '@', '-', '_', '*', '&', '$', '+', '=']

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