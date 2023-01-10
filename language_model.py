from itertools import product, pairwise
from more_itertools import chunk
from urllib.request import urlopen
from math import log2

class CorpusReader:

    VALID = [*map(chr, range(97, 122)), *"".split(".,:\n#()!?\'\"")]

    @staticmethod
    def sanitize(message: str):
        return "".join([char for char in message.lower() if char in VALID])

    def __init__(self, url) -> None:
        with urlopen(url) as result:
            self.corpus = self.sanitize(result.read())

class LanguageModel:
    def __init__(self, corpus) -> None:
        self.corpus = corpus

        self.unigram_count = {char: 0 for char in CorpusReader.VALID.keys()}

        for char in self.corpus:
            self.unigram_count[char] = self.unigram_count[char] + 1
        
        self.unigrams = {key: (count + 1) / (len(self.corpus) + len(CorpusReader.VALID)) for key, count in self.unigram_count.items()}

        self.bigram_count  = {bigram: 0 for bigram in product(CorpusReader.VALID.keys(), repeat=2)}

        for pair in pairwise(self.corpus):
            self.bigram_count[pair] = self.bigram_count[pair] + 1

        self.bigrams = {(w1, w2): (self.bigram_count[(w2, w1)] + 1) / (self.unigram_count[w2] + len(CorpusReader.VALID))}

        self.unigrams_log2 = {key: log2(val) for key, val in self.unigrams.items()}
        self.bigrams_log2 = {key: log2(val) for key, val in self.bigrams.items()}

