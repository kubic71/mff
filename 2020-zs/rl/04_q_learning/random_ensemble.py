import sys
import os
import numpy as np

total = 5

q_files = ["c" + str(i) + ".npy" for i in range(1, total + 1)]
ensemble_file = "ensemble.1"

threshold = 260



while True:
    q = np.zeros((63000, 4))
    weights = [np.random.random() for i in range(len(q_files))]

    for i, fn in enumerate(q_files):
        print(fn)
        q += np.load(fn) * weights[i]

    np.save(ensemble_file, q)

    os.system("./evaluate.sh " + ensemble_file + " | tail -n1 > score")

    with open("score", "r") as f:
        score = float(f.read())

        print("Score:", score)
        if score > threshold:
            print("new best: ", score)

            ensemble_best = f"ensemble,score={score}," + ",".join(list(map(lambda x: str(x)[:6], weights)))
            np.save(ensemble_best, q)


