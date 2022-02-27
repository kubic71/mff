from collections import defaultdict
from email.policy import default
import itertools
import math

def load_data(path):
    with open(path) as file:
        data = file.read().strip().split('\n')
    
    words, tags = [], []
    for line in data:
        l = line.split("/")
        words.append(l[0])
        tags.append(l[1])
    
    return words, tags

def get_unigram_counts(data):
    unigrams = defaultdict(lambda: 0)
    for word in data:
        unigrams[word] += 1
    return unigrams


def get_bigram_probs(data):
    """
    Compute bigram probabilities.
    
    data: list of words
    N: total number of words
    filter: function to filter out words
    """

    bigrams = defaultdict(lambda: 0)
    for i in range(len(data) - 1):
        # TODO: is this correct? 
        # Refering to the assignment:
        # >  Ignore the other words for building the classes, 
        # > but keep them in the data for the bigram counts and 
        # > all the formulas that use them (including the Mutual Information, 
        # > the interim sums in the "Tricks", etc.). 

        bigrams[data[i], data[i+1]] += 1
    
    return normalize(bigrams)


def normalize(bigrams):
    """Normalize bigram probabilities, so they sum to 1."""
    N = sum(bigrams.values())
    normalized = defaultdict(lambda: 0)

    for bigram, count in bigrams.items():
        normalized[bigram] = count / N

    return normalized


def init_unigram_probs(bigrams, left=True):
    """Marginal unigram probabilities from bigram probabilities."""
    unigrams = defaultdict(lambda: 0)

    for bigram, prob in bigrams.items():
        l, r = bigram
        if left:
            unigrams[l] += prob
        else:
            unigrams[r] += prob

    # check, if all unigrams sum to 1 (reasonably close)
    # assert abs(sum(unigrams.values()) - 1) < 0.001

    return unigrams


def cartesian_sum(matrix, rows, cols):
    """
    Sum values of 2-D matrix over the cartesian product of rows and cols arguments.

    q: q(l, r)
    rows: rows of q
    cols: cols of q
    """
    res = 0 
    for row in rows:
        for col in cols:
            res += matrix[row, col]
    return res

def sub(s, q, a, b):
    return s[a] + s[b] - q[a, b] - q[b, a]

def pmi(prob_ab, prob_a, prob_b):
    # print(prob_ab, prob_a, prob_b)
    if prob_ab == 0:
        return 0

    res = prob_ab * (math.log2(prob_ab) - math.log2(prob_a) - math.log2(prob_b))
    return res

def q_macro(bi_prob, uni_l, uni_r, rows, cols):
    """
        Compute q(rows, cols) from bigram and marginal unigram probabilities as if rows and cols were merged.   
    """

    # compute the merged bigram probability
    p_r_c = cartesian_sum(bi_prob, rows, cols)

    # compute the merged unigram probabilities
    # TODO: maybe swap this
    p_row = sum(uni_l[row] for row in rows)
    p_col = sum(uni_r[col] for col in cols)

    return pmi(p_r_c, p_row, p_col)


def add(bi_prob, p_l, p_r, classes, a, b):
    # notation: a+b means union of a and b (as if a and b were merged)
    # we need to add:
    #  q(x, a+b), x not in [a, b]
    #  q(a+b, y), y not in [a, b]
    #  q(a+b, a+b)

    res = 0

    merged = {a, b}
    new_classes = classes - merged

    for c in new_classes:
        res += q_macro(bi_prob, p_l, p_r, merged, {c})
        res += q_macro(bi_prob, p_l, p_r, {c}, merged)

    res += q_macro(bi_prob, p_l, p_r, merged, merged)

    return res


def merge(a, b):
    return a + "/" + b

def update_s(s, q, q_new, a, b, classes):
    """
        s, q are from the previous iteration
        a, b are classes to be merged
        classes is the set of classes after the merge
    """
    raise NotImplementedError
    new_s = defaultdict(lambda: 0)
    for i in classes:
        pass
        # new_s[i] = s[i] - q[i, a] - q[a, i] - q[i, b] - q[b, i] + 

def update_q(q, a, b, classes):
    # merging a and b
    raise NotImplementedError


def compute_word_classes(data, target_num_classes, min_word_count=10, dataset_cutoff=None):

    # Words, that appear in the data at least min_word_count times
    # If dataset_cutoff is not None, take only first dataset_cutoff words
    words_considered = []
    if dataset_cutoff is not None:
        data = data[:dataset_cutoff]

    # add special token to the beginning of the data
    data = ["<s>"] + data

    word_counts = get_unigram_counts(data)
    words_considered = {word for word in word_counts if word_counts[word] >= min_word_count}

    print("Number of words considered:", len(words_considered))
    bigrams = get_bigram_probs(data)

    # check, that the number of bigrams is the square of the number of words considered
    print("Number of unique bigrams:", len(bigrams))

    classes = words_considered.copy()
    # TODO: maybe it's okay to disregard the ends of the dataset and consider p_l == p_r
    p_l = init_unigram_probs(bigrams, left=True)
    p_r = init_unigram_probs(bigrams, left=False)

    big_words = set()
    for l, r in bigrams.keys():
        big_words.add(l)
        big_words.add(r)
    print("Number of unique words in bigrams:", len(big_words))

    while len(classes) > target_num_classes:

        # init q(l, r), which are the probability-weighted point-wise mutual informations
        # TODO: maybe we want to compute q(l, r) from counts instead of probabilities for better numerical stability
        q = defaultdict(lambda: 0)
        for bigram, prob in bigrams.items():
            l, r = bigram
            q[l, r] = pmi(prob, p_l[l], p_r[r])

        # compute the sum of the q(l, r) values, i.e. the mutual information I(D,E)
        I = sum(q.values())
        print("before merge I(D, E):", I)

        # pre-compute the sub values
        # s[k] ... sum of row q(*, k) and column q(k, *)
        s = {}
        for k in classes:
            s[k] = cartesian_sum(q, rows=(k, ), cols=classes)
            s[k] += cartesian_sum(q, rows=classes, cols=(k, ))
            s[k] -= q[k, k]
        

        # for each pair a, b, compute the I(D, E) after the potential merge of a and b
        # and pick the pair with the highest I(D, E)
        max_I = float("-inf")
        best_pair = None
        for a, b in itertools.combinations(classes, 2):
            new_I = I - sub(s, q, a, b) + add(bigrams, p_l, p_r, classes, a, b)
            if new_I > max_I:
                max_I = new_I
                best_pair = (a, b)

        # merge classes
        print("Merging:", best_pair)
        print("max I(D, E):", max_I)
        a, b = best_pair
        #print("Merging", a, "and", b, "with L", L[min_pair])
        classes.remove(a)
        classes.remove(b)

        new_class = merge(a, b)

        new_bigrams = defaultdict(lambda: 0)

        for bigram, prob in bigrams.items():
            # throw away bigrams containing a or b
            l, r = bigram
            if l == a or l == b or r == a or r == b:
                continue

            new_bigrams[l, r] = prob

        # add the new class to the bigrams
        for c in classes:
            new_bigrams[new_class, c] = cartesian_sum(bigrams, rows=(a, b), cols=(c, ))
            new_bigrams[c, new_class] = cartesian_sum(bigrams, rows=(c, ), cols=(a, b))
        
        new_bigrams[new_class, new_class] = cartesian_sum(bigrams, rows=(a, b), cols=(a, b))
        bigrams = new_bigrams

        # copy old bigram
        # new_bigrams = {}
        # for bigram, prob in bigrams.items():
        #     l, r = bigram
        #     if l in classes and r in classes:
        #         new_bigrams[l, r] = prob

        # add new bigrams with the merged class


        # update p
        p_l = init_unigram_probs(new_bigrams, left=True)
        p_r = init_unigram_probs(new_bigrams, left=False)

        # add new merged class to the set of classes
        classes.add(new_class)


    return classes


def print_classes(classes):
    for c in classes:
        print(" ".join(c.split("/")))


if __name__ == '__main__':
    print("started")

    path = "datasets/TEXTEN1.ptg"
    print("loading data")
    words, tags = load_data(path)

    print("Number of unique words:", len(set(words)))

    print("computing word classes, stopping at 15 classes")
    classes = compute_word_classes(words, target_num_classes=15, min_word_count=10, dataset_cutoff=8000)

    print_classes(classes)



    print("getting unigram counts")
    uni = get_unigram_counts(words)
    print(uni["WHEN"])


