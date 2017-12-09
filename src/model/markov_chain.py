from collections import defaultdict


class MarkovChain():
    def __init__(self, n_tuples, order):
        self.freq_dist = build_freq_dist(n_tuples, order)
        self.chain = build_chain(self.freq_dist, order)
        self.order = order

    def for_word(self, word):
        return self.chain[word]

    def __contains__(self, item):
        return item in self.chain

    ########################
    ### Static Functions ###
    ########################

def build_freq_dist(n_tuples, order):
    """
    Takes an iterable of n-tuples, and - for each of those tuples - returns the probability of the
    last item in the tuple following the previous sequence of items

    This will work with any input of tuples composed of strings, i.e.:
    [("4", "3", "2"), ("3", "3", "1"), ..., ("5", "1", "2")] # For sentence lengths
    [("the", "quick", "brown"), ("quick", "brown", "fox"), ..., ("the", "lazy", "fox")] # for words

    :param n_tuples:
    :return a dict of dicts, mapping words to frequency distributions of each word appearing after it:
    """

    if order == 1:
        # Handle the unigram case
        # (Maybe this can be handled in the general algorithm)
        freq_dist = defaultdict(int)
        num_words = len(n_tuples)
        for i in n_tuples:
            key = i[0]
            if key in freq_dist:
                freq_dist[key] += 1
            else:
                freq_dist[key] = 1

        return freq_dist
    else:
        freq_dist = defaultdict(list)

        for g in n_tuples:
            # order-gram keys will be stored as strings separated by KEY_DELIMITER
            freq_dist[KEY_DELIMITER.join(g[:-1])].append(g[-1])

        for seq in freq_dist.keys():
            possible_next = freq_dist[seq] # list of words ["hello", "this", "list", "hello", "can", "repeat", "repeat"]
            num_next = len(possible_next)
            unq_next = set(possible_next)

            count_dict = {}
            for u in unq_next:
                count_dict[u] = possible_next.count(u)

            freq_dist[seq] = count_dict

        return freq_dist

def build_prob_dist(freq_dist):
    '''
    Takes a frequency distribution, and converts it into a probability distribution
    The values no longer represent the count of the key, but the probability of the key.
    All the values in the output dictionary sum to 1.

    :param freq_dist:
    :return prob_dist:
    '''
    prob_dist = {}
    total = sum(freq_dist.values())
    for key in freq_dist:
        count = freq_dist[key]
        prob_dist[key] = count/total
    return prob_dist

def build_chain(freq_dist, order):
    '''
    Takes a group of frequency distributions (stored in a dict) and returns the same structure converted
    to probability distributions
    :param freq_dist:
    :param order:
    :return:
    '''
    if(order == 1):
        return build_prob_dist(freq_dist)
    else:
        for key in freq_dist:
            freq_dist[key] = build_prob_dist(freq_dist[key])
        return freq_dist