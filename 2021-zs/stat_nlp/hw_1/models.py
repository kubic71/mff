import math
from collections import defaultdict

class NGram:
    def __init__(self, n, data):
        self.n = n
        self.ngrams = defaultdict(lambda: 0)
        self._ngrams_num = 0

        self.build(data)

    def build(self, text):
        for i in range(len(text) - self.n + 1):
            ngram = tuple(text[i:i+self.n])
            self.ngrams[ngram] += 1
            self._ngrams_num += 1
    

    def get_ngram_count(self, ngram):
        return self.ngrams[ngram]
    

class NGramLanguageModel:
    def __init__(self, data, n):
        self.ngrams = NGram(n, data)
        self.contexts = NGram(n-1, data)
        self.vocab = set(data)
    
    def cond_prob(self, word, context):
        context = tuple(context)
        c = self.contexts.get_ngram_count(context)
        if c == 0:
            return 0
        return self.ngrams.get_ngram_count(context + (word,)) / c

    def get_ngram_prob(self, ngram):
        return self.ngrams.get_ngram_count(ngram) / self.ngrams._ngrams_num

    def get_model_conditional_entropy(self):
        """Conditional entropy of the word distribution given the context
           computed as:
                -sum of P(w, c) * log(P(w|c))
        """

        s = 0
        for ngram in self.ngrams.ngrams.keys():
            p = self.get_ngram_prob(ngram)
            s += p * math.log2(self.cond_prob(ngram[-1], ngram[:-1]))
        return -s
    
    def get_model_perplexity(self):
        """Perplexity of the model computed as:
            2^H(w|c)
        """
        return 2**self.get_model_conditional_entropy()
