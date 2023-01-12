from language_model import LanguageModel, CorpusReader
from math import exp
from random import random
from permutation import Permutation, ID

class SimulatedAnnealing:
    def __init__(self, temp, thresh, rate) -> None:
        self.temp = temp
        self.thresh = thresh
        self.rate = rate

    def run(self, message, model: LanguageModel):
        hypo = ID
        temp = self.temp
        p = 0
        round = 0
        while temp > self.thresh:
            round += 1
            hypo_ = hypo.get_neighbor()
            delta = hypo_.get_energy(message, model) - hypo.get_energy(message, model)
            if delta < 0:
                p = 1
            else:
                p = exp(-1 * delta / temp)
            if random() > p:
                hypo = hypo_
            
            temp = self.rate * temp
        return hypo