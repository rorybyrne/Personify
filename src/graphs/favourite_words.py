import ronald_brain.util.preprocessor as preprocessor
import ronald_brain.util.constants as constants
from ronald_brain.util.preprocessor import Ngram
from ronald_brain.models.markov_chain import *

from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
from pprint import pprint

import pandas as pd

def favourite_english_words(user):
    user_twitter = constants.TWITTER_ACCOUNTS[user]
    pp = preprocessor.Preprocessor(user_twitter)
    count = Counter(pp.words_only_flat)
    labels, values = zip(*count.items())

    word_dict = {"word" : labels, "count": values}
    df = pd.DataFrame(word_dict)

    df = df.loc[df['count'] > 250]

    sns_plot = sns.factorplot(x='word', y='count', data=df, kind='bar', aspect=2)
    # sns_plot.savefig("graphs/histograms/english_word_count.png")

    plt.show()


def words_after_word(user, target_word, n):
    user_twitter = constants.TWITTER_ACCOUNTS[user]
    pp = preprocessor.Preprocessor(user_twitter)
    words = [t for t in pp.tokenized_flat if t not in USELESS_PUNCTUATION + FRONT_PUNCTUATION]

    grams = pp.build_n_grams(words, n)

    grams = [(','.join(g[:-1]), g[-1]) for g in grams]
    # target_bigrams = [t for t in grams if t[0] == target_word]

    target_follow = [' '.join(t[1:]) for t in grams]

    count = Counter(target_follow)
    labels, values = zip(*count.items())

    word_dict = {"word": labels, "count": values}
    df = pd.DataFrame(word_dict).sort_values('count', ascending=False)

    df = df.head(30)
    pprint(df)

    sns_plot = sns.factorplot(x='word', y='count', data=df, kind='bar', aspect=2)
    sns_plot.savefig("graphs/%s/histograms/word_after_%s_%sgram_count100.png" % (user_twitter, target_word, n))

    plt.show()


# favourite_english_words("DONALD_TRUMP")
word = "unigrams"
words_after_word("DONALD_TRUMP", word, 1)



