import os
import itertools
import time
import random
import os

max_c = 6

num_cuda_executing = 0

# epsilon=1,epsilon_final=0.1,epsilon_final_at=0.4,episodes=3000,gamma=0.99,hidden_size=24,lr=0.003,target_update_freq=200,train_freq=100,buffer_size=500000

seed = [13]

# controller_size = [32, 64]
controller_size = [64]
controller_depth = [2]
tau = [1]


epsilon = [0.3]
epsilon_final = [0.05]
epsilon_final_at = [1]

total_timesteps = [500000]

gamma = [0.99]

target_update_freq = [5000]
train_freq = [8]
green_penalty=[0.75]

frame_skip = [1]
context_length = [1]

batch_size = [2048]
discrete_actions = [True]


def number_of_running_instances():
    return int(os.popen("ps aux | grep \"python carRacingDdpg.py\" | wc -l").read().strip()) - 2

variants = list(itertools.product(green_penalty, seed, context_length, controller_size, controller_depth, epsilon, epsilon_final, epsilon_final_at, total_timesteps, gamma, target_update_freq, train_freq, frame_skip, batch_size, discrete_actions, tau))
random.shuffle(variants)



for gp, s, cl, cs, cd, e, ef, efa, tt, g, tuf, tf, fs, bs, da, t in variants:
    # num_cuda_executing = number_of_running_instances(True)
    
    # if num_cuda_executing < 3:
        # cuda = True
    # else:
        # cuda = False

    # os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    
    cmd = f"python carRacingDdpg.py --render_every=5 --discrete_actions --green_penalty={gp} --tau={t} --seed={s} --context_length={cl} --controller_size={cs} --controller_depth={cd} --epsilon={e} --epsilon_final={ef} --epsilon_final_at={efa} --total_timesteps={tt} --gamma={g} --target_update_interval={tuf} --train_freq={tf} --frame_skip={fs} --batch_size={bs} &"
    print(f"Executing: $ {cmd}")
    os.system(cmd)


    while number_of_running_instances() >= max_c:
        time.sleep(1)