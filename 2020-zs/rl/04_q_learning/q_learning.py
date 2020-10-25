#!/usr/bin/env python3
import argparse

import gym
import numpy as np

import wrappers

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--recodex", default=False,
                    action="store_true", help="Running in ReCodEx")

parser.add_argument("--render_each", default=2000, type=int,
                    help="Render some episodes.")
parser.add_argument("--seed", default=45, type=int, help="Random seed.")

#  For these and any other arguments you add, ReCodEx will keep your default value.

# TODO: try to swap it
parser.add_argument("--decrease_epsilon", default=False, action="store_true")
parser.add_argument("--decrease_alpha", default=True, action="store_true")

parser.add_argument("--episodes", default=2000, type=int, help="Training episodes")
parser.add_argument("--alpha", default=0.5, type=float, help="Learning rate.")
parser.add_argument("--epsilon", default=0.5, type=float,
                    help="Exploration factor.")
parser.add_argument("--gamma", default=1, type=float,
                    help="Discounting factor.")

def epsilon_schedule(args, episode):
    # exponentially descrease epsilon
    return args.epsilon * 0.5**(5 * episode/args.episodes)

def alpha_schedule(args, episode):
    # exponentially descrease alpha learning rate
    return args.alpha * 0.5**(5 * episode/args.episodes)

def main(env, args):
    def epsilon_greedy(action, epsilon):
        if np.random.random() < epsilon:
            # random action
            return np.random.randint(0, env.action_space.n)
        else:
            # greedy action
            return action

    # Fix random seed
    np.random.seed(args.seed)

    # TODO: Variable creation and initialization
    q = np.zeros((env.observation_space.n, env.action_space.n))

    for e in range(args.episodes):
        # Perform episode
        state, done = env.reset(), False
        while not done:
            if args.render_each and env.episode > 0 and env.episode % args.render_each == 0:
                env.render()

            action = epsilon_greedy(np.argmax(q[state]), epsilon_schedule(args, e) if args.decrease_epsilon else args.epsilon)
            next_state, reward, done, _ = env.step(action)

            # TODO: Update the action-value estimates
            q[state, action] = q[state, action] + (alpha_schedule(args, e) if args.decrease_alpha else args.alpha) * (reward + args.gamma*np.max(q[next_state]) - q[state, action])
            state = next_state

    # Final evaluation
    while True:
        state, done = env.reset(start_evaluation=True), False
        while not done:
            # TODO: Choose (greedy) action
            action = np.argmax(q[state])
            state, reward, done, _ = env.step(action)


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)

    # Create the environment
    env = wrappers.EvaluationWrapper(wrappers.DiscreteMountainCarWrapper(
        gym.make("MountainCar1000-v0")), args.seed, logname=f"alpha={args.alpha},epsilon={args.epsilon},gamma={args.gamma},de={args.decrease_epsilon},da={args.decrease_alpha},seed={args.seed}", evaluate_for=100)

    main(env, args)

