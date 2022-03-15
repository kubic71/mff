from collections import defaultdict
import itertools
import math
from time import clock_settime
from matplotlib.pyplot import cla
import tqdm
import os

def load_data(path):
    with open(path) as file:
        data = file.read().strip().split('\n')
    
    words, tags = [], []
    for line in data:
        l = line.split("/")
        words.append(l[0])
        tags.append(l[1])
    
    return words, tags


def init_bigram_and_unigram_counts(words):
    c_l = defaultdict(lambda: 0)
    c_r = defaultdict(lambda: 0)
    c = defaultdict(lambda: 0)

    for i in range(len(words) - 1):
        c_l[words[i]] += 1
        c_r[words[i+1]] += 1
        c[words[i], words[i+1]] += 1

    return c_l, c_r, c


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

def merge(a, b):
    return a + "/" + b

def compute_word_classes(data, target_num_classes, output_fn, min_word_count=10, N=8000):
    
    output_file = open(output_fn, "w")

    def print_and_write(string):
        print(string)
        output_file.write(string + "\n")
        output_file.flush()

    # Words, that appear in the data at least min_word_count times
    # If dataset_cutoff is not None, take only first dataset_cutoff words

    assert N <= len(data)
    data = data[:N] 

    # add special token to the beginning of the data
    special_token = "<s>"
    data = [special_token] + data


    c_l, c_r, c = init_bigram_and_unigram_counts(data)
    
    classes = {word for word in c_r if c_r[word] >= min_word_count}
    print_and_write(f"{len(classes)} considered classes: {' '.join(sorted(classes))}\n")


    all_classes = set(c_r.keys())
    all_classes.add(special_token)


    def pmi(ab_counts, counts_a, counts_b):
        if ab_counts == 0:
            return 0
        return  ab_counts / N * math.log2(N * ab_counts / (counts_a * counts_b))

    def q_macro(rows, cols):
        """
            Compute q(rows, cols) from bigram and marginal unigram probabilities as if rows and cols were merged.   
        """

        # compute the merged bigram probability
        p_r_c = cartesian_sum(c, rows, cols)

        # compute the merged unigram probabilities
        # TODO: maybe swap this
        p_row = sum(c_l[row] for row in rows)
        p_col = sum(c_r[col] for col in cols)

        return pmi(p_r_c, p_row, p_col)


    def add(all_classes, a, b):
        # notation: a+b means union of a and b (as if a and b were merged)
        # we need to add:
        #  q(x, a+b), x not in [a, b]
        #  q(a+b, y), y not in [a, b]
        #  q(a+b, a+b)

        res = 0

        merged = (a, b)

        for c in all_classes:
            if c == a or c == b:
                continue
            res += q_macro(merged, (c, ))
            res += q_macro((c,), merged)

        res += q_macro(merged, merged)

        return res

    def sub(a, b, q, s):
        return s[a] + s[b] - q[a, b] - q[b, a]

    # init q
    print("Initializing q...")
    q = {}
    for l in all_classes:
        for r in all_classes:
            q[l, r] = pmi(c[l, r], c_l[l], c_r[r])

    # init s
    print("Initializing s...")
    s = {}
    for a in all_classes:
        s[a] = 0
        for w in all_classes:
            s[a] += q[w, a] + q[a, w]
        s[a] -= q[a, a]

    # for a, b in c:
    #     s[a] += q[b, a]
    #     s[a] += q[a, b]   
    
    # for a in all_classes:
    #     s[a] -= q[a, a]


    def L_get(L, a, b):
        if (a, b) in L:
            return L[a, b]
        else:
            return L[b, a]

    # init L
    print("Initializing L...")
    L = {}
    for a, b in tqdm.tqdm(list(itertools.combinations(classes, 2))):
        L[a, b] = sub(a, b, q, s) - add(all_classes, a, b)
    

    def update_counts(a, b, classes):

        ab = merge(a, b)
        c_l[ab] = c_l[a] + c_l[b]
        c_r[ab] = c_r[a] + c_r[b]


        for cl in classes:
            c[cl, ab] = c[cl, a] + c[cl, b]
            c[ab, cl] = c[a, cl] + c[b, cl]
        
        c[ab, ab] = c[a, a] + c[a, b] + c[b, a] + c[b, b]


    
    def update_q(q, a, b, classes):
        ab = merge(a, b)
        q2 = q.copy()

        for i, j in q:
            if i == a or i == b or j == a or j == b:
                del q2[i, j]

        # add q(x, a+b) for x not in [a, b]

        for i in classes:
            if i == a or i == b:
                continue
            q2[i, ab] = pmi(c[i, ab], c_l[i], c_r[ab])
            q2[ab, i] = pmi(c[ab, i], c_r[i], c_l[ab])

        q2[ab, ab] = pmi(c[ab, ab], c_r[ab], c_l[ab])
        
        return q2


    def update_s(s, q, q2, a, b, classes):
        
        ab = merge(a, b)
        s2 = defaultdict(lambda: 0)

        for i in classes:
            if i == a or i == b:
                continue
              
            s2[i] = s[i] - q[i, a] - q[a, i] - q[i, b] - q[b, i] + q2[ab, i] + q2[i, ab]


        # s2(ab) must be computed using the "Init" sum
        for i in classes:
            if i == a or i == b:
                continue

            assert i != ab
            s2[ab] += q2[i, ab] + q2[ab, i]
        
        s2[ab] += q2[ab, ab]

        return s2

    def update_L(L, q, q2, s, s2, a, b, classes, new_all_classes):
        ab = merge(a, b)

        L2 = {}
        for i, j in itertools.combinations(classes, 2):
            if i == a or i == b or j == a or j == b:
                continue

            L2[i, j] = L_get(L, i, j) - s[i] + s2[i] - s[j] + s2[j]
            L2[i, j] += q_macro((i, j), (a,)) + q_macro((a,), (i, j)) + q_macro((i, j), (b,)) + q_macro((b,), (i, j))
            L2[i, j] -= q_macro((i, j), (ab,)) - q_macro((ab,), (i, j))

        # L2[ab, i] and L2[i, ab] must be computed using the "Init" sum

        for i in classes:
            if i == a or i == b:
                continue

            assert i != ab
            L2[ab, i] = sub(ab, i, q2, s2) - add(new_all_classes, ab, i)

        return L2

    def update_classes(classes, a, b):
        new_c = classes.copy()
        new_c.remove(a)
        new_c.remove(b)
        new_c.add(merge(a, b))

        return new_c



    print("Initializing I")
    I = 0
    for l in all_classes:
        for b in all_classes:
            I += q[l, b]

    while len(classes) > target_num_classes:
        # print(len(classes), len(all_classes))

        
        # compute the sum of the q(l, r) values, i.e. the mutual information I(D,E)
        # I = sum(q.values())

        # print("I(D, E):", I)

        # for each pair a, b, compute the I(D, E) after the potential merge of a and b
        # and pick the pair with the highest I(D, E)
        max_I = float("-inf")
        best_pair = None
        for a, b in itertools.combinations(classes, 2):
            new_I = I - L_get(L, a, b)
            if new_I > max_I:
                max_I = new_I
                best_pair = (a, b)

        a, b = best_pair

        out_str = f"|{len(classes)}. I(D, E): {I}, loss: {I - max_I}, merging:\n{class_to_str(a)}\n{class_to_str(b)}\n"
        print_and_write(out_str)


        # merge classes
        I = max_I

        #print("Merging", a, "and", b, "with L", L[min_pair])
        new_classes = update_classes(classes, a, b)
        new_all_classes = update_classes(all_classes, a, b)

        update_counts(a, b, all_classes)

        q2 = update_q(q, a, b, all_classes)

        s2 = update_s(s, q, q2, a, b, all_classes)

        # classes == considerer classes (not all classes)
        L2 = update_L(L, q, q2, s, s2, a, b, classes, new_all_classes)

        q = q2
        s = s2
        L = L2
        classes = new_classes
        all_classes = new_all_classes

    print_and_write(f"\n\nFinal {len(classes)} classes:")

    for c in classes:
        print_and_write(class_to_str(c))

    output_file.close()

    return classes


def class_to_str(cl):
    # return " ".join(sorted(cl.split("/")))
    return " ".join(cl.split("/"))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=None, help="Dataset cutoff size")
    parser.add_argument("--target_num_classes", type=int, default=15, help="Stop merging when this many classes are reached")
    parser.add_argument("--dataset_path", type=str, default="datasets/TEXTEN1.ptg")

    parser.add_argument("--mode", type=str, choices=["words", "tags"], default="words", help="Whether to use words or tags as classes to be merged")


    args = parser.parse_args()

    if args.mode == "words":
        min_word_count = 10
    else:
        min_word_count = 5


    if args.dataset_path.endswith("EN1.ptg"):
        lang = "EN"
    elif args.dataset_path.endswith("CZ1.ptg"):
        lang = "CZ"
    else:
        raise ValueError("Unknown dataset")



    print("loading data")
    words, tags = load_data(args.dataset_path)

    data = words if args.mode == "words" else tags

    print("Number of unique datapoints:", len(set(data)))


    if args.N is None or args.N > len(data):
        args.N = len(data)

    results_fn = f"results/merge_results_{args.mode}_{lang}_N-{args.N}_target_num-{args.target_num_classes}.txt"

    classes = compute_word_classes(data, target_num_classes=args.target_num_classes, output_fn=results_fn, min_word_count=min_word_count, N=args.N)

