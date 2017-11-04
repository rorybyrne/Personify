from ronald_brain.util.preprocessor import *
from ronald_brain.util.constants import TWEET_REGEXES, FRONT_PUNCTUATION, USELESS_PUNCTUATION
from wordcloud import WordCloud
from wordcloud.tokenization import unigrams_and_bigrams, process_tokens

import matplotlib.pyplot as plt

import csv

class TweetCloud(WordCloud):
    '''
    Subclassing the WordCloud class to implement our own tokenizer for Twitter data
    '''
    def process_text(self, text):
        print("inside")
        stopwords = set([i.lower() for i in self.stopwords])
        regexp = re.compile(r'(' + '|'.join(TWEET_REGEXES) + ')', re.VERBOSE | re.IGNORECASE)

        words = re.findall(regexp, text)
        # remove stopwords
        words = [word for word in words if word.lower() not in stopwords]

        words = [word for word in words if word not in FRONT_PUNCTUATION + USELESS_PUNCTUATION]
        # remove 's
        words = [word[:-2] if word.lower().endswith("'s") else word
                 for word in words]
        # remove numbers
        words = [word for word in words if not word.isdigit()]

        if self.collocations:
            word_counts = unigrams_and_bigrams(words, self.normalize_plurals)
        else:
            word_counts, _ = process_tokens(words, self.normalize_plurals)

        return word_counts

def create_word_cloud(file_name):
    pp = Preprocessor(file_name)
    raw_data = pp.tweets_as_string()
    wc = TweetCloud(width=800, height=400).generate(raw_data)

    return wc

def save_cloud(wordcloud):
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('graphs/wordclouds/tweet_total_cloud.png')

