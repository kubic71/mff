#!/usr/bin/env python3
import argparse

import gym
import numpy as np

import wrappers


parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--recodex", default=False, action="store_true", help="Running in ReCodEx")
parser.add_argument("--render_each", default=2000, type=int, help="Render some episodes.")
parser.add_argument("--seed", default=1, type=int, help="Random seed.")

# For these and any other arguments you add, ReCodEx will keep your default value.
parser.add_argument("--logdir", default='logs', type=str)
parser.add_argument("--alpha", default=0.5, type=float, help="Learning rate.")
parser.add_argument("--alpha_dec", default=5, type=float, help="Learning rate.")

parser.add_argument("--epsilon", default=0.5, type=float )
parser.add_argument("--epsilon_final", default=0.1, type=float, help="Final exploration factor.")
parser.add_argument("--epsilon_final_at", default=0.3, type=float, help="Percentage of total training episodes.")
parser.add_argument("--load_from", type=str, default="best.npy")

parser.add_argument("--episodes", default=2000, type=int)
parser.add_argument("--gamma", default=1, type=float, help="Discounting factor.")
parser.add_argument("--tiles", default=32, type=int, help="Number of tiles.")
parser.add_argument("--copy_every", default=0, type=int)


def alpha_schedule(args, episode):
    # exponentially descrease alpha learning rate
    return args.alpha * 0.5**(args.alpha_dec * episode/args.episodes)

def epsilon_greedy(action, epsilon):
    return np.random.randint(env.action_space.n) if np.random.random() < epsilon else action

def main(env, args):
    # Fix random seed
    global W
    np.random.seed(args.seed)


    # Implement Q-learning RL algorithm, using linear approximation.
    W = np.zeros([env.observation_space.nvec[-1], env.action_space.n], dtype="float64")
    W1 = np.zeros([env.observation_space.nvec[-1], env.action_space.n], dtype="float64")

    if args.recodex:
        W = np.load(args.load_from)

    epsilon = args.epsilon

    for i in range(0 if args.recodex else args.episodes):
        if args.copy_every > 0 and env.episode % args.copy_every == 0:
            W1 = np.copy(W)

        # Perform episode
        state, done = env.reset(), False
        while not done:
            if args.render_each and env.episode and env.episode % args.render_each == 0:
                env.render()

            # TODO: Choose an action.
            summed_q_values = W[state].sum(axis=0)
            action = epsilon_greedy(np.argmax(summed_q_values), epsilon)

            next_state, reward, done, _ = env.step(action)

            #print(state, next_state, action, reward)
            # print(W[state, action])
            # W[state, action] = W[state, action] + args.alpha * (reward + args.gamma*np.max(W[next_state].sum(axis=0)/args.tiles) - W[state, action])
            target = W1 if args.copy_every > 0 else W
            W[state, action] = W[state, action] + alpha_schedule(args, env.episode) / args.tiles * (reward + args.gamma*np.max(target[next_state].sum(axis=0)) - W[state, action].sum())

            state = next_state

        
        if args.epsilon_final_at:
            epsilon = np.interp(env.episode + 1, [0, args.epsilon_final_at * args.episodes], [args.epsilon, args.epsilon_final])


    try:
        # Final evaluation
        returns = []
        while True:
            state, done = env.reset(start_evaluation=True), False

            r = 0
            while not done:
                action = np.argmax(W[state].sum(axis=0))
                state, reward, done, _ = env.step(action)
                r += reward
            returns.append(r)
    except KeyboardInterrupt:
        if not args.recodex:
            np.save(f"{sum(returns)}_{args.tiles}_W_matrix.npy", W)


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)

    # Create the environment

    env = wrappers.EvaluationWrapper(wrappers.DiscreteMountainCarWrapper(gym.make("MountainCar1000-v0"), tiles=args.tiles), args.seed, logname=f"{args.logdir}/alpha={args.alpha},alpha_dec={args.alpha_dec},epsilon={args.epsilon},epsilon_final={args.epsilon_final},epsilon_final_at={args.epsilon_final_at},episodes={args.episodes},tiles={args.tiles},gamma={args.gamma},seed={args.seed}")
    main(env, args)

