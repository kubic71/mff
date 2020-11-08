import sys
import numpy as np


ensemble_file = "ensemble.1"

# q_files = [
#     ("alpha=0.00234375,alpha_dec_exp=3,epsilon=0.1,gamma=0.99,n=10,expert_every=2,episodes=10000,seed=4", 2),
#     ("alpha=0.00234375,alpha_dec_exp=3,epsilon=0.1,gamma=0.99,n=20,expert_every=2,episodes=10000,seed=4", 10),
#     ("alpha=0.6,alpha_dec_exp=8,epsilon=0.1,gamma=0.99,n=10,expert_every=2,episodes=100000,seed=4", 1)]

q_files = [
    ("alpha=0.00234375,alpha_dec_exp=3,epsilon=0.1,gamma=0.99,n=10,expert_every=2,episodes=10000,seed=4", 2),
    ("best", 4),
    ("q1_best", 1),
    ("q2_best", 1),
    ("q1", 1),
    ("q2", 1),
    ("alpha=0.6,alpha_dec_exp=8,epsilon=0.1,gamma=0.99,n=10,expert_every=2,episodes=100000,seed=4", 1)]
q = np.zeros((63000, 4))


for q_file, weight in q_files:

    q += np.load(q_file + ".npy") * weight
    
np.save(ensemble_file, q)
