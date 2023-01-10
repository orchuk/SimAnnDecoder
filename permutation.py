from random import choices
from language_model import LanguageModel
from itertools import pairwise

class Permutation:
    def __init__(self, cypher) -> None:
        self.cypher = cypher

    def get_neighbor(self):
        a, b = choices(self.cypher.keys(), k=2)
        new_cypher = self.cypher
        new_cypher[a], new_cypher[b] = new_cypher[b], new_cypher[a]
        return Permutation(new_cypher)

    def translate(self, encrypted):
        return "".join([self.chyper[char] for char in encrypted])

    def get_energy(self, encrypted, model: LanguageModel):
        return -1 * (model.unigrams_log2[encrypted[0]] + sum([model.bigrams_log2[(w2, w1)] for (w1, w2) in pairwise(encrypted[1:], 2)]))