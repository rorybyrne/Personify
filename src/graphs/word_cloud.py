import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from wordcloud import WordCloud
from wordcloud.tokenization import unigrams_and_bigrams, process_tokens

from util import TWEET_REGEXES, FRONT_PUNCTUATION, USELESS_PUNCTUATION


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

def create_word_cloud(user):
    pp = Preprocessor(user)

    wc = TweetCloud(width=2000, height=2200,
                    background_color="#001610",
                    stopwords=set(stopwords.words('english'))).generate(' '.join(pp.words_only_flat))

    return wc

def save_cloud(wordcloud):
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    # plt.show()
    plt.savefig('graphs/wordclouds/tweet_total_cloud.png')

user = "realdonaldtrump"
cloud = create_word_cloud(user)
cloud.to_file('graphs/wordclouds/%s_tweet_cloud.png')


