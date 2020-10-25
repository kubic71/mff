import os
import itertools
import time
import random

max_c = 16

epsilon = [0.5]
gamma = [1]
alpha = [0.5]
seed = [1,2,3,4,5,6,7,8]

decrease_epsilon = [False]
decrease_alpha = [True]


def number_of_running_instances():
    return int(os.popen("ps aux | grep \"python q_learning.py\" | wc -l").read().strip()) - 2




variants = list(itertools.product(epsilon, gamma, alpha, decrease_epsilon, decrease_alpha, seed))
random.shuffle(variants)

for e, g, a, de, da, s in variants:
    cmd = f"python q_learning.py --epsilon={e} --gamma={g} --alpha={a} --seed={s} " + ("--decrease_epsilon " if de else "") + ("--decrease_alpha " if da else "") + "--episodes=1000&"
    print(f"Executing: $ {cmd}")
    os.system(cmd)

    while number_of_running_instances() >= max_c:
        time.sleep(1)