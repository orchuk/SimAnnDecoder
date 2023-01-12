import itertools
import string
from urllib.request import urlopen
from math import log2

class CorpusReader:
    """
    Read an online corpus.
    """

    VALID = {*string.ascii_lowercase, ".", ",", ":", "\n", "#", "(", ")", "!", "?", "\'", "\"", " "}

    @classmethod
    def sanitize(cls, message: str):
        """
        Clean up undesired characters.
        """
        res = []
        for char in message:
            if char in cls.VALID:                   # append valid char
                res.append(char)
            elif char in string.ascii_uppercase:    # lowercase valid uppercase
                res.append(char.lower())

        return "".join(res).lower()                 # return string

    def __init__(self, url) -> None:
        """
        Read the corpus.
        """
        with urlopen(url) as result:                # open a remote resource
            res = str(result.read())

            self.corpus = self.sanitize(res)        # clean up result

            self.unigram_count = {char: 0 for char in self.VALID}

            for char in self.corpus:                # count unigrams
                self.unigram_count[char] = self.unigram_count[char] + 1

            self.bigram_count  = {bigram: 0 for bigram in itertools.product(self.VALID, repeat=2)}

            for pair in itertools.pairwise(self.corpus):
                self.bigram_count[pair] += 1        # count bigrams

class LanguageModel:
    def __init__(self, corpus: CorpusReader) -> None:
        self.corpus = corpus

        # compute n-gram frequencies
        self.unigrams = {key: (count + 1) / (len(self.corpus.corpus) + len(self.corpus.VALID)) for key, count in self.corpus.unigram_count.items()}
        self.bigrams = {(w1, w2): (self.corpus.bigram_count[(w2, w1)] + 1) / (self.corpus.unigram_count[w2] + len(self.corpus.VALID)) for (w1, w2) in self.corpus.bigram_count.keys()}
       
       # log2 frequencies
        self.log2unigrams = {w: log2(val) for w, val in self.unigrams.items()}
        self.log2bigrams = {(w1, w2): log2(val) for (w1, w2), val in self.bigrams.items()}