#!/usr/bin/env python3
# 3619d41d-b80b-11e7-a937-00505601122b
# 7cf40fc2-b294-11e7-a937-00505601122b

import argparse
import collections
import os

import gym
import torch as th
from gym.wrappers.time_limit import TimeLimit
import numpy as np
from typing import Union, List

# from stable_baselines3 import SAC

# from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback, BaseCallback

import wrappers

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--recodex",
                    default=True,
                    action="store_true",
                    help="Running in ReCodEx")
parser.add_argument("--render_each",
                    default=0,
                    type=int,
                    help="Render some episodes.")
parser.add_argument("--seed", default=42, type=int, help="Random seed.")

parser.add_argument("--threads",
                    default=1,
                    type=int,
                    help="Maximum number of threads to use.")

parser.add_argument("--timesteps", default=150000, type=int)
parser.add_argument("--learning_rate", default=7.3e-4, type=float)
parser.add_argument("--buffer_size", default=300000, type=int)
parser.add_argument("--batch_size", default=256, type=int)
parser.add_argument("--tau", default=0.02, type=float)
parser.add_argument("--gamma", default=0.98, type=float)
parser.add_argument("--train_freq", default=64, type=int)
parser.add_argument("--gradient_steps", default=64, type=int)
parser.add_argument("--net_arch", default=[400, 300], type=List[int])

parser.add_argument("--load_from", default="best_model.zip", type=str)

parser.add_argument("--tensorboard_log_dir",
                    default="/tmp/stable-baselines",
                    type=str)
parser.add_argument("--log_interval", default=10, type=int)


def lr_schedule(t):
    # exponential lr schedule
    decay_factor = 50
    c = args.timesteps / np.math.log(decay_factor, 2)
    return args.learning_rate * 0.5**((1-t) * args.timesteps / c)


def get_exp_name():
    return "WalkerGeneric"


# For these and any other arguments you add, ReCodEx will keep your default value.
"""
class EpisodeCallback(BaseCallback):
    def __init__(self, env):
        verbose = 1
        self.env = env
        super(EpisodeCallback, self).__init__(verbose)

    def _on_step(self):
        if self.n_calls % 100 == 0:
            print(self.n_calls / 100)

        if self.n_calls > 50000:
            self.env._max_episode_steps = 800
"""
def load_actor():
    seq = th.nn.Sequential(
            th.nn.Linear(in_features=24, out_features=400, bias=True),
            th.nn.ReLU(),
            th.nn.Linear(in_features=400, out_features=300, bias=True),
            th.nn.ReLU(),
            th.nn.Linear(in_features=300, out_features=4, bias=True),
            th.nn.Hardtanh(min_val=-2, max_val=2)
    )

    sd = seq.state_dict()




    it = np.load('best.npy', allow_pickle=True)

    wb = {}
    for key, val in it:
        wb[key] = val


    w0 = wb['latent_pi.0.weight']
    b0 = wb['latent_pi.0.bias']
    w1 = wb['latent_pi.2.weight']
    b1 = wb['latent_pi.2.bias']
    w2 = wb['mu.weight']
    b2 = wb['mu.bias']

    sd['0.weight'].copy_(w0)
    sd['0.bias'].copy_(b0)
    sd['2.weight'].copy_(w1)
    sd['2.bias'].copy_(b1)
    sd['4.weight'].copy_(w2)
    sd['4.bias'].copy_(b2)

    return seq


def main(env, args):
    th.set_num_threads(1)
    global model
    # Fix random seeds and number of threads
    np.random.seed(args.seed)

    if args.recodex:
        model = load_actor()
        # model = SAC.load(args.load_from)

        while True:
            state, done = env.reset(start_evaluation=True), False
            while not done:
                action = model(th.tensor(np.array([state], dtype=np.float32)))[0].data.numpy()
                ## TODO delete before submitting
                # env.render()

                state, reward, done, _ = env.step(action)

    else:

        tensorboard_log_dir = None if args.tensorboard_log_dir is None else os.path.join(
            args.tensorboard_log_dir, get_exp_name())

        model = SAC("MlpPolicy",
                    env,
                    learning_rate=lr_schedule,
                    buffer_size=args.buffer_size,
                    learning_starts=10000,
                    batch_size=args.batch_size,
                    tau=args.tau,
                    gamma=args.gamma,
                    train_freq=args.train_freq,
                    gradient_steps=args.gradient_steps,
                    ent_coef="auto",
                    use_sde=False,
                    policy_kwargs=dict(log_std_init=-3,
                                       net_arch=args.net_arch),
                    tensorboard_log=tensorboard_log_dir,
                    seed=args.seed)

        model.verbose = 2

        callbacks = [
            CheckpointCallback(10000,
                               "checkpoints",
                               name_prefix=get_exp_name()),
            EvalCallback(gym.make("BipedalWalker-v3"),
                         callback_on_new_best=SaveBestModelCallback(),
                         eval_freq=10000,
                         n_eval_episodes=5,
                         deterministic=True)
            # EpisodeCallback(env)
        ]

        print(args.log_interval)
        model.learn(args.timesteps,
                    log_interval=args.log_interval,
                    callback=callbacks)



if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)

    # Create the environment
    if not args.recodex:
        # env = TimeLimit(
        env = wrappers.EvaluationWrapper(
            gym.make("BipedalWalkerHardcore-v3"), evaluate_for=100, seed=args.seed)
                        # max_episode_steps=1600)
    else:
        env = wrappers.EvaluationWrapper(gym.make("BipedalWalkerHardcore-v3"),
                                         seed=args.seed)

    main(env, args)
