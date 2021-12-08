import math
from collections import defaultdict

def ngram_iterator(data, n):
    """Return an iterator yielding context and word pairs."""
    for i in range(len(data)-n):
        yield tuple(data[i:i+n]), data[i+n]


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
    

class LinearInterpolationModel:
    """Language model linearly interpolating n-grams of multiple orders."""
    def __init__(self, training_data, n):
        self.training_data = training_data
        self.n = n

        self.ngram_models = [None]
        for i in range(1, n + 1):
            self.ngram_models.append(NGram(i, training_data))
        
        # weights of individual n-gram models, that sum up to 1
        self.lambdas = [1 / len(self.ngram_models)] * len(self.ngram_models)

        self.vocab = set(training_data)

    def _ngram_prob(self, word, context, n):
        assert type(context) == tuple
        """probability of word given context of n-gram model of order n"""

        if n == 0:
            # zero-th order n-gram model outputs uniform probability 1/|V|
            return 1 / len(self.vocab)

        elif n == 1:
            # unigram model gives frequency of the word in the training data divided by the training data size
            return  self.ngram_models[1].get_ngram_count((word,)) / len(self.training_data)

        else:
            # higher order n-gram model gives frequency of the (context, word) in the training data divided by the frequency of the context

            # clip the context to the length n-1
            context = context[-n+1:]

            c1 = self.ngram_models[n].get_ngram_count(context + (word,))
            c2 = self.ngram_models[n-1].get_ngram_count(context)
            
            if c1 > 0 and c2 > 0:
                return c1 / c2
            return 0


    def prob(self, word, context):
        """probability of a word given some context"""
        assert type(context) == tuple
        result = 0

        # print(f"p({word} | {context}) = ", end="")


        # for each n-gram model, calculate the probability of the word given the context weigthed by the lambda
        # and add it to the result
        # s = []
        for i in range(0, len(self.ngram_models)):
            p = self._ngram_prob(word, context, i)
            # s.append(f"{self.lambdas[i]}*{p}")
            result += self.lambdas[i] * p

        # print(f"{' + '.join(s)} = {result}")

        return result

    def _expected_counts(self, heldout_data, j):
        """Calculate expected counts of j-th lambda in the heldout_data"""
        c = 0

        for context, word in ngram_iterator(heldout_data, self.n):
            c += self.lambdas[j] * self._ngram_prob(word, context, j) / self.prob(word, context)

        return c


    def fit_lambdas(self, heldout_data, epsilon=0.0001):
        """Find lambdas which minimize the cross entropy of the model on heldout_data using the EM algorithm

            args: 
                heldout_data: list of words to be used as heldout data
                epsilon: minimum difference between two consecutive lambdas to continue the EM algorithm
        """

        i = 1

        # initialize lambdas to uniform distribution
        self.lambdas = [1 / len(self.ngram_models)] * len(self.ngram_models)

        print(f"Initial lambdas: " + ", ".join(map(str, self.lambdas)))
        while True:
            # E-step
            counts = [self._expected_counts(heldout_data, j) for j in range(len(self.lambdas))]

            # M-step
            new_lambdas = [c / sum(counts) for c in counts]

            step_size = max([abs(new_l - old_l) for new_l, old_l in zip(new_lambdas, self.lambdas)])

            print(f"{i}. cross-entropy: {self.cross_entropy(heldout_data):.9f}\tlambda-delta: {round(step_size, 6)}\tlambdas: {' '.join(map(lambda l: str(round(l, 5)), new_lambdas))}")

            # check if we converged
            if step_size < epsilon:
                break

            self.lambdas = new_lambdas
            i += 1


        print("\n\n")
        return self.lambdas
    
    def cross_entropy(self, data):
        """Calculate the cross entropy of the model on some text data"""

        s = 0
        num_ngrams = 0
        for context, word in ngram_iterator(data, self.n):
            p = self.prob(word, context)
            assert p > 0
            s += math.log(p)
            num_ngrams += 1
        
        return -s / num_ngrams



class NGramLanguageModel:
    def __init__(self, data, n):
        self.ngrams = NGram(n, data)
        self.contexts = NGram(n-1, data)
        self.vocab = set(data)
    
    def cond_prob(self, word, context):
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
