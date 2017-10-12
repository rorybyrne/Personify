import random
import sys
import ronald_brain.constants as constants

from ronald_brain import utils


class Generator:
    """
    This class will hold all of our models (there's a separate model
     per 2,3,n-gram of words, sentence length, and POS tag etc.)
    It contains functions which use those models to generate text.
    All models are created when the class is initialized with a filename.
    The entrypoint to get the next word is currently predict_next()
    """
    def __init__(self, sourcefile, word_ngrams=2):
        """
        Here we initialize the Generator by creating all the models necessary

        :param sourcefile:
        :param word_ngrams:
        """
        self.sourcefile = sourcefile
        self.word_n = word_ngrams
        # we store a unique n-gram model for each n=2 -> n
        self.word_ngram_models = self.build_word_models(self.word_n) # TODO: Add unigram building into build_word_models()

    def build_word_models(self, n):
        """
        Wecursively build a list of models for n > 2.
        We want a list of models so that we can implement the Backoff algorithm
        https://www.quora.com/What-is-backoff-in-NLP

        :param models:
        :return a list of n-gram models:
        """
        if(n < 1):
            # TODO: Exception
            sys.exit(0)

        if n == 1:
            return [utils.unigram_probs(self.sourcefile)]
        else:
            m = utils.get_n_gram_probs(self.sourcefile, n)
            return self.build_word_models(n-1) + [m]

    def predict_next(self, ngram):
        # split the ngram by ',' to get the # of words.
        n = len(ngram.split(constants.WORD_KEY_DELIMITER))
        print("Ngram as key: " + ngram)
        if n == 0:
            # TODO: Exception
            sys.exit(0)
        if n == 1:
            # if we are given a unigram, use unigram model
            return self._weighted_choice(self.word_ngram_models[0])

        # otherwise get the appropriate ngram model
        current_model = self.word_ngram_models[n]
        # If either of these checks fails, we want to backoff to an n-1gram
        if ngram in current_model and len(current_model[ngram]) > 3:
            choice = self._weighted_choice(current_model[ngram])
            return choice
        else:
            backoff_words = ngram.split(',')[1:]
            print("BackingOff...from " + str(n) + " to " + str(len(backoff_words)))
            print("Backoff words: " + ', '.join(backoff_words))
            backoff_ngram = ','.join(backoff_words)
            return self.predict_next(backoff_ngram)


    def _weighted_choice(self, dict):
        """
            dict is of the form { event : probability,
                                    event : probability,
                                    ...,
                                    event : probability }
            We randomly pick an event, but the randomness depends on the probabilities

            :param dict:
            :return a weighted random choice of key from the dict:
            """
        r = random.uniform(0, 1)  # 1 is the total of our probability distribution
        tmp = 0.0

        for k in dict:
            tmp += dict[k]
            if r < tmp:
                return k

    def generate(self, num_words):
        # "i" and "am" are basically the seed words, to begin the sentence with.
        # will need to figure out a way for the system to choose this word intelligently
        # https://github.com/RoryOfByrne/ronald-trump/issues/4
        output = ["we", "are", "going", "to"]
        for x in range(num_words):
            leng = len(output)
            # keys in the probability distribution are comma-separated: "first_word,second_word"
            prev = constants.WORD_KEY_DELIMITER.join(output[leng - self.word_n + 1:])
            print("prev: " + prev)
            next_word = self.predict_next(prev)
            print("next word: " + next_word)
            output.append(next_word)
            print("\n")
        return ' '.join(output)