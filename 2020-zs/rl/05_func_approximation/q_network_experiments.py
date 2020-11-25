import os
import itertools
import time
import random

max_c = 16
# epsilon=1,epsilon_final=0.1,epsilon_final_at=0.4,episodes=3000,gamma=0.99,hidden_size=24,lr=0.003,target_update_freq=200,train_freq=100,buffer_size=500000

seed = [8]
hidden_size = [24]
learning_rate = [0.03, 0.08, 0.18]

epsilon = [1]
epsilon_final = [0.1]
epsilon_final_at = [0.5]

episodes = [6000]

gamma = [0.99]

target_update_freq = [200]
train_freq = [10, 30]

buffer_size = [5000, 50000]
batch_size = [256, 512]


def number_of_running_instances():
    return int(os.popen("ps aux | grep \"python q_network.py\" | wc -l").read().strip()) - 2

variants = list(itertools.product(seed, hidden_size, learning_rate, epsilon, epsilon_final, epsilon_final_at, episodes, gamma, target_update_freq, train_freq, buffer_size, batch_size))
random.shuffle(variants)



for s, hs, lr, e, ef, efa, ep, g, tuf, tf, buf_s, bs in variants:
    cmd = f"python q_network.py --seed={s} --hidden_layer_size={hs} --learning_rate={lr} --epsilon={e} --epsilon_final={ef} --epsilon_final_at={efa} --gamma={g} --episodes={ep} --target_update_freq={tuf} --train_freq={tf} --buffer_size={buf_s} --batch_size={bs} &"
    print(f"Executing: $ {cmd}")
    os.system(cmd)

    while number_of_running_instances() >= max_c:
        time.sleep(1)