from plot import *

plot_file("out/t-sequential-std", None, "Sequential test - standard splay")
plot_file("out/t-sequential-naive", None, "Sequential test - naive splay")

plot_file("out/t-random-std", None, "Random test - standard splay", logscale=True)
plot_file("out/t-random-naive", None, "Random test - naive splay", logscale=True)

plot_file_subset("out/t-subset-std", "Subset test - standard splay")
plot_file_subset("out/t-subset-naive", "Subset test - naive splay")
