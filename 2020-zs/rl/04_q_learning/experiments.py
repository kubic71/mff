import os
import itertools
import time
import random

max_c = 16
# alpha=0.6,alpha_dec_exp=8,epsilon=0.1,gamma=0.99,n=10,expert_every=2,episodes=100000,seed=4


start_epsilon = [1]
target_epsilon = [0.1]
gamma = [0.999]
alpha = [0.6]
alpha_decay_exp = [8]

n = [20]
expert_every = [5]

seed = [10]

epsilon_decay = [True]
alpha_decay = [True]


episodes = [400000]

evaluate_for = 5000

def number_of_running_instances():
    return int(os.popen("ps aux | grep \"python lunar_lander_double.py\" | wc -l").read().strip()) - 2

variants = list(itertools.product(target_epsilon, start_epsilon, gamma, alpha, epsilon_decay, alpha_decay, expert_every, n, seed, episodes, alpha_decay_exp))
random.shuffle(variants)



for e, es, g, a, de, da, ex, n, s, ep, a_dec_exp in variants:
    checkpoint_str = f"double=True,alpha={a},alpha_dec_exp={a_dec_exp},epsilon={e},start_epsilon={es},gamma={g},n={n},expert_every={ex},episodes={ep},seed={s}"
    cmd = f"python lunar_lander_double.py --evaluate_for={evaluate_for} --epsilon={e} --start_epsilon={es} --gamma={g} --alpha={a} --save_to={checkpoint_str} --alpha_decay_exp={a_dec_exp} --seed={s} --episodes={ep} --expert_training_every={ex} --n={n} " + ("--epsilon_decay " if de else "") + ("--alpha_decay " if da else "") + "&"
    print(f"Executing: $ {cmd}")
    os.system(cmd)

    while number_of_running_instances() >= max_c:
        time.sleep(1)