import ronald_brain.util.preprocessor as preprocessor
import ronald_brain.util.constants as constants
from ronald_brain.util.preprocessor import Ngram

def favourite_words():
    pp = preprocessor.Preprocessor(constants.CSV_FILE_LOCATION)
    unigram_model = pp.build_model_list(1, Ngram.WORD)[0]
