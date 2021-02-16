class SuffixArray:
    def __init__(self, text):
        self.text = text
        # S is the suffix array (a permutation which sorts suffixes)
        # R is the ranking array (the inverse of S)
        self.R, self.S = self._build_suffix_array(text)
        self.n = len(text)

        # build_lcp runs in O(n)
        self.L = self._build_lcp()

    def _build_suffix_array(self, text):
        """
        Construct the suffix array and ranking array for the given string
        using the doubling algorithm.
        """

        n = len(text)
        R = [None] * (n+1)
        S = [None] * (n+1)

        R = self._sort_and_rank(S, lambda a: ord(text[a]) if a < len(text) else -1)

        k = 1
        while k < n:
            R = self._sort_and_rank(S, lambda a: (R[a], (R[a+k] if a+k < n else -1)))
            k *= 2

        return (tuple(R), tuple(S))

    # An auxiliary function used in the doubling algorithm.
    def _sort_and_rank(self, S, key):
        for i in range(len(S)): S[i] = i
        S.sort(key = key)

        R = [None] * len(S)
        for i, s in enumerate(S):
            prev_s = S[i-1]
            if i == 0 or key(prev_s) != key(s): R[s] = i
            else: R[s] = R[prev_s]
        return R


    def _build_lcp(self):
        # Implementation of Kasai's algorithm running in O(n)

        k = 0
        L = [0] * (self.n + 1)
        for p in range(self.n):
            k = max(k-1, 0)
            i = self.R[p]

            if i == self.n:
                continue

            q = self.S[i + 1]
            while (p + k < self.n) and (q + k < self.n) and (self.text[p + k] == self.text[q + k]):
                k += 1

            L[i] = k
        

        return L

    def num_kgrams(self, k):
        """Return the number of distinct k-grams in the string."""

        num = 0
        for i in range(1, self.n + 1):

            if self.L[i] < k and self.n - self.S[i] >= k:
                num += 1

        return num









if __name__ == "__main__":
    arr = SuffixArray("annbansbananas")
    print(arr.num_kgrams(2))



