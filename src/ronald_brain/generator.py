import random
import ronald_brain.postprocessor as postprocessor
import ronald_brain.constants as constants

from ronald_brain.preprocessor import Ngram
from ronald_brain import preprocessor


class Generator:
    """
    This class will hold all of our models (there's a separate model
        per 2,3,n-gram of words, sentence length, and POS tag etc.).

    All models are created when the class is initialized with a filename.
    The entrypoint to get the next word is predict_next()
    """
    def __init__(self, sourcefile, word_ngrams=2, sent_length_ngrams=2):
        """
        Here we initialize the Generator by creating all the models necessary

        :param sourcefile:
        :param word_ngrams:
        """
        self.sourcefile = sourcefile
        self.preprocessor = preprocessor.Preprocessor(sourcefile)
        self.word_n = word_ngrams
        self.sentence_n = sent_length_ngrams
        self.first_words_n = constants.FIRST_WORDS_N

        # we store a unique n-gram model for each n=2 -> n
        print("Building word n-gram models...")
        word_ngram_models = self.preprocessor.build_ngram_model_list(self.word_n, Ngram.WORD)
        print("Word n-gram models built!\n")

        print("Building sentence-length n-gram models...")
        sentence_ngram_models = self.preprocessor.build_ngram_model_list(self.sentence_n, Ngram.SENT_LENGTH)
        print("Sentence-length n-gram models built!\n")

        print("Building model for first words")
        first_word_models = self.preprocessor.build_ngram_model_list(constants.FIRST_WORDS_N, Ngram.FIRST_WORD)
        print("First words n-gram models built!")

        self.models = {'word': word_ngram_models,
                       'sent_len': sentence_ngram_models,
                       'first_word': first_word_models}

    def predict_next(self, ngram, model):
        """
        Given an ngram, it consults the models to choose the next word.
        This is where the logic for using the models will exist. Right now it's a weighted random choice
            based on word n-grams.
        TODO: Extend this to include some logic using sentence lengths

        :param ngram:
        :return:
        """
        print("Ngram as key: " + ngram)

        # if we are given a unigram, use unigram model
        if ngram == '': # use unigram model
            model = self.models[model][0]
            foo = self.weighted_choice(model)
            print(foo)
            return foo

        n = len(ngram.split(constants.KEY_DELIMITER))

        # otherwise get the appropriate ngram model
        if ngram == constants.START_TOKEN:
            # We choose the model differently for the First_Word models
            current_model = self.models[model][self.first_words_n-1]
        else:
            current_model = self.models[model][n]

        # If either of these checks fails, we want to backoff to an n-1gram
        if ngram in current_model and len(current_model[ngram]) > 3:
            choice = self.weighted_choice(current_model[ngram])
            return choice
        else:
            backoff_words = ngram.split(' ')[1:]
            print("BackingOff...from " + str(n) + " to " + str(len(backoff_words)))
            print("Backoff words: " + ' '.join(backoff_words))
            backoff_ngram = ' '.join(backoff_words)
            return self.predict_next(backoff_ngram, model)


    def weighted_choice(self, dict):
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

    def generate_sentence(self, length, seed_words=None):
        '''
        Generates a sentence of len `length`, with optional seed words

        :param length:
        :param seed_words:
        :return:
        '''

        if(seed_words):
            first_word = self.predict_next(constants.KEY_DELIMITER.join(seed_words), 'word')
        else:
            # First word prediction looks like "w1 w1 ... wn", so we split by space
            # Splitting by X returns the same string if there's no X
            first_word = self.predict_next(constants.START_TOKEN, 'first_word').split(constants.KEY_DELIMITER)

        output = first_word # first_word is a list [<WORD>] because of the str.split() above

        while(len(output) < length):
            count = len(output)

            # keys in the probability distribution are comma-separated: "first_word,second_word"
            if(count < self.word_n):
                prev = constants.KEY_DELIMITER.join(output)
            else:
                prev = constants.KEY_DELIMITER.join(output[-self.word_n + 1:])

            next_word = self.predict_next(prev, 'word')
            output.append(next_word)

        return output



    def generate(self, char_count):
        # The way of choosing the first words is a little hacky
        next_len = int(self.predict_next('', 'sent_len')) # Predictions are always strings. So we convert to int
        output = []

        char_total = 0

        while(True):
            if(char_total > char_count):
                break
            sentence = self.generate_sentence(next_len)
            sent_string = ' '.join(sentence)
            output.append(sent_string)

            next_len = int(self.predict_next(str(len(output[-1])), 'sent_len')) # Predict the next sent_length

            char_total += len(sent_string)

        raw_output = ' '.join(output[:-1]) # We drop the last sentence because it put us over the limit
        return postprocessor.run(raw_output)