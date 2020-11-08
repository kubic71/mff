import numpy as np
import sys
import os


def save(q):
    i = 1
    while True:
        fn = "b" + str(i) + ".npy"
        if fn in os.listdir():
            i += 1
            continue

        np.save(fn, q)
        return

q1, q2 = np.load(sys.argv[1])
if len(sys.argv) > 2:
    np.save(sys.argv[2], q1)
    np.save(sys.argv[3], q2)
else:
    save(q1)
    save(q2)


