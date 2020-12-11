#!/usr/bin/env python3
import argparse
import collections
import os

import gym
from gym.wrappers.time_limit import TimeLimit
import numpy as np
from typing import Union, List

from stable_baselines3 import SAC

from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback, BaseCallback

import wrappers

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--recodex",
                    default=False,
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

parser.add_argument("--timesteps", default=1000000, type=int)
parser.add_argument("--frame_skip", default=4, type=int)
parser.add_argument("--learning_rate", default=0.0014, type=float)
parser.add_argument("--buffer_size", default=600000, type=int)
parser.add_argument("--batch_size", default=256, type=int)
parser.add_argument("--tau", default=0.015, type=float)
parser.add_argument("--gamma", default=0.99, type=float)
parser.add_argument("--train_freq", default=256, type=int)
parser.add_argument("--gradient_steps", default=64, type=int)
parser.add_argument("--no-render", default=False, action="store_true")
parser.add_argument("--net_arch", default=[400, 300], type=int, nargs="+")

# !! TODO change to True
parser.add_argument("--hardcore", default=True, action="store_true")

parser.add_argument("--load_from", default=None, type=str)

parser.add_argument("--tensorboard_log_dir",
                    default="/tmp/stable-baselines2",
                    type=str)
parser.add_argument("--log_interval", default=10, type=int)

def getEnvName():
    return "BipedalWalker" + ("Hardcore" if args.hardcore else "") + "-v3"

def lr_schedule(t):
    # exponential lr schedule
    decay_factor = 10
    c = args.timesteps / np.math.log(decay_factor, 2)
    lr = args.learning_rate * 0.5**((1-t) * args.timesteps / c)


    # linear warmup for 2% of the training
    if (1-t) < 0.02:
        lr = (1-t)/0.02 * lr

    return lr


def get_exp_name():
    return f"{getEnvName()}-lr={args.learning_rate},fs={args.frame_skip},tau={args.tau},gamma={args.gamma},n={args.timesteps},tau={args.tau},train_freq={args.train_freq},grad_steps={args.gradient_steps},bs={args.batch_size},buf_size={args.buffer_size},net_arch={','.join(list(map(str, args.net_arch)))}"


class SaveBestModelCallback(BaseCallback):
    def __init__(self, save_path="best/best_model.zip", verbose=1):
        super(SaveBestModelCallback, self).__init__(verbose)
        self.save_path = save_path

    def _on_step(self):
        print("Saving best model.." + self.save_path)
        globals()['model'].save(self.save_path)


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


def main(env, args):
    global model
    # Fix random seeds and number of threads
    np.random.seed(args.seed)

    if args.recodex:
        model = SAC.load(args.load_from)

        while True:
            state, done = env.reset(start_evaluation=True), False
            while not done:
                # action, _states = model.predict(state, deterministic=True)
                action, _states = model.predict(state)

                ## TODO delete before submitting
                if not args.no_render:
                    env.render()

                state, reward, done, _ = env.step(action)

    else:

        tensorboard_log_dir = None if args.tensorboard_log_dir is None else os.path.join(
            args.tensorboard_log_dir, get_exp_name())

        model = SAC("MlpPolicy",
                    env,
                    learning_rate=lr_schedule,
                    buffer_size=args.buffer_size,
                    # learning_starts=10000,
                    learning_starts=5000,
                    batch_size=args.batch_size,
                    tau=args.tau,
                    gamma=args.gamma,
                    train_freq=args.train_freq,
                    gradient_steps=args.gradient_steps,
                    ent_coef="auto",
                    use_sde=False,
                    policy_kwargs=dict(log_std_init=-3,
                                       net_arch=args.net_arch, use_expln=True),
                    tensorboard_log=tensorboard_log_dir,
                    seed=args.seed)

        model.verbose = 2

        callbacks = [
            CheckpointCallback(20000,
                               "checkpoints",
                               name_prefix=get_exp_name()),
            EvalCallback(gym.make(getEnvName()),
                         callback_on_new_best=SaveBestModelCallback(save_path="best/" + get_exp_name() + "_best_model.zip"),
                         eval_freq=20000,
                         n_eval_episodes=5,
                         deterministic=True)
            # EpisodeCallback(env)
        ]

        print(args.log_interval)
        model.learn(args.timesteps,
                    log_interval=args.log_interval,
                    callback=callbacks)


        # Final evaluation
        env = wrappers.EvaluationWrapper(gym.make(getEnvName()), evaluate_for=200, seed=args.seed)

        while True:
            state, done = env.reset(start_evaluation=True), False
            while not done:
                action, _states = model.predict(state, deterministic=True)
                state, reward, done, _ = env.step(action)


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)

    # Create the environment
    if not args.recodex:
        # env = TimeLimit(
        env = wrappers.EvaluationWrapper(
            gym.make(getEnvName()), evaluate_for=10, seed=args.seed)
                        # max_episode_steps=1600)

        if args.frame_skip > 1:
            env = wrappers.FrameSkipWrapper(env, args.frame_skip)
    else:
        env =  wrappers.EvaluationWrapper(gym.make(getEnvName()),
                                         seed=args.seed)

    main(env, args)
