import random
from decimal import *


class VoseSort:
    """
    A class used to generate discrete probability distributions.
    For an EXCELLENT write up and source of this algorithm, see:
        http://www.keithschwarz.com/darts-dice-coins/
    This current implementation is based largely on asmith26's, though I re-wrote it for learning purposes.
        https://github.com/asmith26/Vose-Alias-Method
    """

    def __init__(self, probabilities):
        self.prob_dist = probabilities  # To receive probabilities; passed in as a dict {obj: probability}
        self.prob_table = {}  # probability table
        self.alias_table = {}  # An alias reference to probability dict.
        self.populate_worklists()

    def populate_worklists(self):
        scaled_probs = {}
        n = len(self.prob_dist)  # number of probabilities.
        working_large = []  # Working list for calculated probabilities over 1
        working_small = []  # Working list for calculated probabilities under 1

        for obj, prob in self.prob_dist.items():
            scaled_probs[obj] = Decimal(prob) * n

            if scaled_probs[obj] < 1:
                working_small.append(obj)
            else:
                working_large.append(obj)

        while working_large and working_small:
            large = working_large.pop()
            small = working_small.pop()
            self.prob_table[small] = scaled_probs[small]
            self.alias_table[small] = large
            scaled_probs[large] = (scaled_probs[large] - scaled_probs[small]) - Decimal(1)
            if scaled_probs[large] < 1:
                working_small.append(large)
            else:
                working_large.append(large)

        # The remaining outcomes of 1 stack must be 1.
        while working_large:
            self.prob_table[working_large.pop()] = Decimal(1)

        while working_small:
            self.prob_table[working_small.pop()] = Decimal(1)

    def alias_generation(self):
        col = random.choice(list(self.prob_table))

        if self.prob_table[col] >= random.uniform(0, 1):
            return col
        else:
            return self.alias_table[col]
