import nltk.data

FRONT_PUNCTUATION = [',', '.', '?', '!', ':', ';']
USELESS_PUNCTUATION = ['(', ')', '"', '\'', '^', '@', '-']

def run(text):
    text = remove_useless_punctuation(text)
    text = fix_punctuation(text)
    text = capitalize_sentences(text)
    return text

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

def remove_double_space(text):
    return text.replace('  ', ' ')

def capitalize_sentences(text):
    tok = nltk.data.load("tokenizers/punkt/english.pickle")
    sentences = tok.tokenize(text)
    return ' '.join([s[0].upper() + s[1:] for s in sentences])