import re

FRONT_PUNCTUATION = [',', '.', '?', '!', ':', ';']

def fix_punctuation(text):
    output = text
    for p in FRONT_PUNCTUATION:
        output = output.replace(r' ' + p, p)

    return output