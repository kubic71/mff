import sys

with open(sys.argv[1], "r") as f:
    bins = [0 for i in range(10)]

    for line in f.read().strip().split("\n"):
        weight, bin_i = list(map(int, line.split()))
        bins[bin_i] += weight

print("max(bins) - min(bins) =", max(bins) - min(bins))
    