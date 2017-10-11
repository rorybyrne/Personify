import random
import utils

class Generator:
    """
    This class will hold all of our models (there's a separate model
     per 2,3,n-gram of words, sentence length, and POS tag etc.)
    It contains functions which use those models to generate text.
    All models are created when the class is initialized with a filename.
    The entrypoint to get the next word is currently predict_next()
    """
    def __init__(self, sourcefile, word_ngrams=2):
        self.sourcefile = sourcefile
        self.word_ngrams = word_ngrams
        # we store a unique n-gram model for each n=2 -> n
        self.word_ngram_models = self.build_word_model(word_ngrams, [])

    def build_word_model(self, models):
        """
        recursively build a list of models for n > 2

        :param models:
        :return a list of n-gram models:
        """
        n = self.word_ngrams
        if n < 2:
            # todo: check that models is not empty
            return models
        else:
            m = utils.get_n_gram_probs(self.sourcefile, n)
            return [m] + self.build_word_model(n-1)

    def predict_next(self, probs, current):
        n = self.word_ngrams
        if current in self.word_ngram_models[n-1]:
            choice = self._weighted_choice(probs[current])
            return choice
        return "UNK"


    def _weighted_choice(self, dict):
        """
            dict is of the form { event : probability,
                                    event : probability,
                                    ...,
                                    event : probability }
            We randomly pick an event, but the randomness depends on the probabilities

            :param dict:
            :return:
            """
        r = random.uniform(0, 1)  # 1 is the total of our probability distribution
        tmp = 0.0

        for k in dict:
            tmp += dict[k]
            if r < tmp:
                return k

n = 3
probs = utils.get_n_gram_probs("/home/rory/projects/ronald/data/trump-tweets.csv", n)

# this is basically the seed word, to begin the sentence with.
# will need to figure out a way for the system to choose this word intelligently
# https://github.com/RoryOfByrne/ronald-trump/issues/4
w1 = "you"
w2 = "own"
output = [w1, w2]
x = 0
while x < 30:
    leng = len(output)
    # keys in the probability distribution are comma-separated: "first_word,second_word"
    prev = ','.join(output[leng-n+1:])
    next_word = predict_word(probs, prev)[0]
    output.append(next_word)
    x += 1

print(' '.join(output))
