import os
import itertools
import time
import random

max_c = 16
# alpha=0.6,alpha_dec_exp=8,epsilon=0.1,gamma=0.99,n=10,expert_every=2,episodes=100000,seed=4

seed = [6]
alpha = [0.5]
alpha_dec = [3, 5]

epsilon = [0.5]
epsilon_final = [0.1]
epsilon_final_at = [0.6, 1]

episodes = [1500]

gamma = [0.99]

tiles = [32, 64]

def number_of_running_instances():
    return int(os.popen("ps aux | grep \"python q_learning_tiles.py\" | wc -l").read().strip()) - 2

variants = list(itertools.product(seed, alpha, alpha_dec, epsilon, epsilon_final, epsilon_final_at, episodes, gamma, tiles))
random.shuffle(variants)



for s, a, ad, e, ef, efa, ep, g, t in variants:
    cmd = f"python q_learning_tiles.py --epsilon={e} --epsilon_final={ef} --epsilon_final_at={efa} --gamma={g} --alpha={a} --alpha_dec={ad} --tiles={t} --seed={s} --episodes={ep} &"
    print(f"Executing: $ {cmd}")
    os.system(cmd)

    while number_of_running_instances() >= max_c:
        time.sleep(1)