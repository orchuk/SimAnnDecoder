from simulated_annealing import SimulatedAnnealing
from language_model import CorpusReader, LanguageModel

if __name__ == "__main__":
    sa = SimulatedAnnealing(1000, 0.00001, 0.9995)
    lm = LanguageModel(CorpusReader("http://www.gutenberg.org/files/76/76-0.txt"))
    with open("problemset_07_encrypted_input.txt") as enc:
        msg    = enc.read()
        result = sa.run(msg, lm)
        print(result.cypher, result.translate(msg), result.get_energy(msg, lm))