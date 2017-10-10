import random
import utils

def predict_word(probs, word):
    if word in probs:
        choice = weighted_choice(probs[word])
        return (choice, probs[word][choice])

    return ("unknown", 0.0)

def weighted_choice(dict):
    r = random.uniform(0, 1) # 1 is the total of our probability distribution
    tmp = 0.0

    for k in dict:
        tmp += dict[k]
        if r < tmp:
            return k
        return k

probs = utils.get_n_gram_probs("/home/rory/projects/ronald/data/trump-tweets.csv", n=3)

next_word = "we"
#print("we" in probs)
#pprint.pprint(dict(probs))
x = 0
while x < 30:
        print(next_word + " ", end='')
        next_word = predict_word(probs, next_word)[0]
        x += 1
