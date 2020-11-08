#!/usr/bin/env python3
import argparse
import sys

import gym
import numpy as np
import os
os.system("mkdir logs")

import wrappers

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--recodex", default=False,
                    action="store_true", help="Running in ReCodEx")
parser.add_argument("--render_each", default=0, type=int,
                    help="Render some episodes.")
parser.add_argument("--evaluate_for", default=100, type=int)

parser.add_argument("--seed", default=42, type=int, help="Random seed.")
# For these and any other arguments you add, ReCodEx will keep your default value.
parser.add_argument("--alpha", default=None, type=float, help="Learning rate.")
parser.add_argument("--epsilon", default=0.5, type=float,
                    help="Exploration factor.")
parser.add_argument("--epsilon_decay", default=False, action="store_true")
parser.add_argument("--alpha_decay", default=False, action="store_true")
parser.add_argument("--alpha_decay_exp", default=5, type=float)

parser.add_argument("--gamma", default=None, type=float,
                    help="Discounting factor.")

parser.add_argument("--expert_training_every", default=2, type=int)
parser.add_argument("--episodes", default=None, type=int,
                    help="Number of training episodes")
parser.add_argument("--n", default=None, type=int, help="Depth of backup tree")
parser.add_argument("--init_random_actions", default=0, type=int)

parser.add_argument("--load_from", default="best",
                    type=str, help="Q starting point")

parser.add_argument("--save_to", default=None,
                    type=str, help="Q checkpoint")

def main(env, args):


    def epsilon_decay(episode):
        # linear decay in first 33% of training episodes from 1 to target epsilon
        start_epsilon = 0.1
        return max(start_epsilon * (1 - 3*episode / args.episodes) + (3*episode / args.episodes * args.epsilon), args.epsilon)
        
    def alpha_decay(episode):
        # exponential decay by a factor of 32 = 2 ** 5
        return args.alpha * 0.5**(episode / args.episodes * args.alpha_decay_exp)


    def epsilon_greedy(action, epsilon):
        if np.random.random() < epsilon:
            # random action
            return np.random.randint(0, env.action_space.n)
        else:
            # greedy action
            return action

    def A(i):
        assert(i >= 0)
        return trajectory[i][0]

    def R(i):
        assert(i >= 1)
        return trajectory[i - 1][1]

    def S(i):
        if i == 0:
            return init_state
        return trajectory[i - 1][2]

    # Fix random seed
    np.random.seed(args.seed)

    if args.load_from is not None:
        if args.load_from + ".npy" in os.listdir():
            print("Loading checkpoint ", args.load_from)
            # if there is checkpoint, load it and start from there
            q = np.load(args.load_from + ".npy")
        else:
            print(args.load_from + ".npy" + " Doesn't exists!")
            sys.exit(1)
    
    else:
        q = np.zeros((env.observation_space.n, env.action_space.n))


    for e in range(0 if args.recodex else args.episodes):
        if e % 100 == 0 and args.save_to is not None:
            np.save(args.save_to, q)


        expert_training = e % args.expert_training_every == 0

        if expert_training:
            init_state, trajectory = env.expert_trajectory()
        else:
            init_state = env.reset()
            trajectory = []

        T = float("inf")  # lenght of an episode

        # print(f"Ep:{e}, epsilon:{epsilon_decay(e)}, alpha:{alpha_decay(e)}")

        t = 0
        while True:

            if t < T:
                if not expert_training:
                    if t < args.init_random_actions:
                        action = np.random.randint(0, env.action_space.n)
                    else:
                        action = epsilon_greedy(np.argmax(q[S(t)]), epsilon_decay(e) if args.epsilon_decay else args.epsilon)

                    state, reward, done, _ = env.step(action)
                    trajectory.append((action, reward, state))

                    if args.render_each and env.episode and env.episode % args.render_each == 0:
                        # print(reward)
                        env.render()

                    if done:
                        T = t + 1

                elif t+1 == len(trajectory):
                    # S(t+1) is terminal
                    T = t + 1

            tau = t + 1 - args.n
            if tau >= 0:
                if t + 1 >= T:
                    G = R(T)
                else:
                    G = R(t + 1) + args.gamma * \
                        np.max(q[S(t + 1)])

                for k in range(min(t, T-1), tau, -1):
                    G = R(k) + args.gamma * (G if A(k) ==
                                             np.argmax(q[S(k)]) else np.max(q[S(k)]))

                lr = alpha_decay(e) if args.alpha_decay else args.alpha
                q[S(tau), A(tau)] = q[S(tau), A(
                    tau)] + lr*(G - q[S(tau), A(tau)])

            if tau == T - 1:
                break

            t += 1


    # Final evaluation
    while True:
        state, done = env.reset(start_evaluation=True), False
        while not done:
            if args.render_each and env.episode and env.episode % args.render_each == 0:
                env.render()
            action = np.argmax(q[state])
            state, reward, done, _ = env.step(action)


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)

    # Create the environment
    env = wrappers.EvaluationWrapper(wrappers.DiscreteLunarLanderWrapper(
        gym.make("LunarLander-v2")), seed=args.seed, logname=f"alpha={args.alpha},alpha_decay_exp={args.alpha_decay_exp},epsilon={args.epsilon},gamma={args.gamma},n={args.n},epsilon_decay={args.epsilon_decay},alpha_decay={args.alpha_decay},expert_every={args.expert_training_every},episodes={args.episodes},seed={args.seed},init_random_actions={args.init_random_actions}", evaluate_for=args.evaluate_for)

    main(env, args)
