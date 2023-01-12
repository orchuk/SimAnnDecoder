from random import choices
from language_model import LanguageModel, CorpusReader
from more_itertools import pairwise
from math import log2

class Permutation:
    def __init__(self, cypher) -> None:
        self.cypher = cypher

    def get_neighbor(self):
        a, b = choices(list(self.cypher.keys()), k=2)
        new_cypher = dict(self.cypher)
        temp = new_cypher[a]
        new_cypher[a] = new_cypher[b]
        new_cypher[b] = temp
        return Permutation(new_cypher)

    def translate(self, encrypted):
        return "".join([self.cypher[char] for char in encrypted])

    def get_energy(self, encrypted, model: LanguageModel):
        return sum([model.log2bigrams[(w2, w1)] for (w1, w2) in pairwise(self.translate(encrypted))])

ID = Permutation({char: char for char in CorpusReader.VALID})