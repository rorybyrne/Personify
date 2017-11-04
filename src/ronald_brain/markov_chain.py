from collections import defaultdict
from .constants import *

class MarkovChain():
    def __init__(self, n_tuples, order):
        self.chain = self.build_chain(n_tuples, order)
        self.order = order

    def build_chain(self, n_tuples, order):
        """
        Takes an iterable of n-tuples, and - for each of those tuples - returns the probability of the
        last item in the tuple following the previous sequence of items

        This will work with any input of tuples composed of strings, i.e.:
        [("4", "3", "2"), ("3", "3", "1"), ..., ("5", "1", "2")] # For sentence lengths
        [("the", "quick", "brown"), ("quick", "brown", "fox"), ..., ("the", "lazy", "fox")] # for words

        :param n_tuples:
        :return a dict of dicts, mapping words to probability distributions of each word appearing after it:
        """

        if order == 1:
            # Handle the unigram case
            # (Maybe this can be handled in the general algorithm)
            prob_dist = defaultdict(int)
            num_words = len(n_tuples)
            for i in n_tuples:
                key = i[0]
                if key in prob_dist:
                    prob_dist[key] += 1
                else:
                    prob_dist[key] = 1

            unq_items = [str(i[0]) for i in set(n_tuples)]

            for k in unq_items:
                prob_dist[k] = prob_dist[k] / num_words

            return prob_dist
        else:
            prob_dist = defaultdict(list)

            for g in n_tuples:
                # order-gram keys will be stored as strings separated by KEY_DELIMITER
                prob_dist[KEY_DELIMITER.join(g[:-1])].append(g[-1])

            for seq in prob_dist.keys():
                possible_next = prob_dist[seq]
                num_next = len(possible_next)
                unq_next = set(possible_next)

                # the probability of each word appearing after the word_seq
                next_prob_dist = {}

                for t in unq_next:
                    next_prob_dist[t] = float(possible_next.count(t)) / num_next
                prob_dist[seq] = next_prob_dist

            return prob_dist

    def for_word(self, word):
        return self.chain[word]

    def __contains__(self, item):
        return item in self.chain