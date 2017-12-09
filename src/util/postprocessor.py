import nltk.data
from .constants import FRONT_PUNCTUATION, USELESS_PUNCTUATION, NUMBER_TWITTER_HANDLE_REGEX, MAX_OVERLAP_RATIO, MAX_OVERLAP_TOTAL

def run(text):
    text = remove_useless_punctuation(text)
    text = fix_punctuation(text)
    text = capitalize_sentences(text)
    return text

def run_pre_ginger(text):
    text = remove_useless_punctuation_and_handles(text)
    text = fix_punctuation(text)
    text = capitalize_sentences(text)
    return text

def matches_corpus(sentence, text):
    # Reject large chunks of similarity
    overlap_ratio = int(round(MAX_OVERLAP_RATIO * len(sentence)))
    overlap_max = min(MAX_OVERLAP_TOTAL, overlap_ratio)
    overlap_over = overlap_max + 1
    gram_count = max((len(sentence) - overlap_max), 1)
    grams = [sentence[i:i + overlap_over] for i in range(gram_count)]
    for g in grams:
        gram_joined = " ".join(g)
        if gram_joined in text:
            print("'%s' is a dublicate of the corpus" % (gram_joined))
            return True
    return False

def fix_punctuation(text):
    output = text
    for p in FRONT_PUNCTUATION:
        output = output.replace(r' ' + p, p)

    return output

def remove_useless_punctuation(text):
    output = text
    for p in USELESS_PUNCTUATION:
        output = output.replace(p, '')
    return remove_double_space(output)

def remove_useless_punctuation_and_handles(text):
    output = text
    output = output.replace(NUMBER_TWITTER_HANDLE_REGEX, '')
    for p in USELESS_PUNCTUATION:
        output = output.replace(p, '')
    return remove_double_space(output)

def remove_double_space(text):
    return text.replace('  ', ' ')

def capitalize_sentences(text):
    tok = nltk.data.load("tokenizers/punkt/english.pickle")
    sentences = tok.tokenize(text)
    return ' '.join([s[0].upper() + s[1:] for s in sentences])