from random import choices
from language_model import LanguageModel, CorpusReader
from more_itertools import pairwise
from math import log2

class Permutation:
    """
    A decryption key.
    """
    def __init__(self, cypher) -> None:

        self.cypher = cypher

    def get_neighbor(self):
        """
        Get a near-identical decryption key.
        """
        a, b = choices(list(self.cypher.keys()), k=2) # select two random entries
        new_cypher = dict(self.cypher)                # duplicate the key
        temp = new_cypher[a]                          # swap
        new_cypher[a] = new_cypher[b]
        new_cypher[b] = temp
        return Permutation(new_cypher)

    def translate(self, encrypted):
        # a translated string is a string where all chars 
        # are decrypted according to the decryption key
        return "".join([self.cypher[char] for char in encrypted]) 

    def get_energy(self, encrypted, model: LanguageModel):
        # the energy of a decryption key is the likelyhood (sum of log-probabilities) 
        # of the decrypted string in the language model
        return sum([model.log2bigrams[(w2, w1)] for (w1, w2) in pairwise(self.translate(encrypted))])

ID = Permutation({char: char for char in CorpusReader.VALID}) # the identity permutation