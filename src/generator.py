import random
import utils

def predict_word(probs, word):
    if word in probs:
        choice = weighted_choice(probs[word])
        return (choice, probs[word][choice])

    return ("unknown", 0.0)

def weighted_choice(dict):
    """
    dict is of the form { word : probability,
                            word : probability,
                            ...,
                            word : probability }
    We randomly pick a word, but the randomness depends on the probabilities

    :param dict:
    :return:
    """
    r = random.uniform(0, 1) # 1 is the total of our probability distribution
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
