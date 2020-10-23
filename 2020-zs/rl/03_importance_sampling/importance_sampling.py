#!/usr/bin/env python3
import argparse

import gym
import numpy as np

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--episodes", default=1000, type=int, help="Training episodes.")
parser.add_argument("--recodex", default=False, action="store_true", help="Running in ReCodEx")
parser.add_argument("--seed", default=42, type=int, help="Random seed.")
# If you add more arguments, ReCodEx will keep them with your default values.

def main(args):
    # Create the environment
    env = gym.make("FrozenLake-v0")
    env.seed(args.seed)
    env.action_space.seed(args.seed)

    # Fix random seed
    np.random.seed(args.seed)

    # Behaviour policy is uniformly random.
    # Target policy uniformly chooses either action 1 or 2.
    V = np.zeros(env.observation_space.n)
    C = np.zeros(env.observation_space.n)

    for _ in range(args.episodes):
        state, done = env.reset(), False

        # Generate episode
        episode = []
        while not done:
            action = env.action_space.sample()
            next_state, reward, done, _ = env.step(action)
            episode.append((state, action, reward))
            state = next_state

        g = 0
        w = 1

        for state, action, reward in reversed(episode):
            # if action other than 1 or 2 was taken by the behavior policy, the probability of this action
            # with respect to the target policy is 0, therefore the weight of this trajectory is also 0 so we can end the episode evaluation
            if action not in (1,2):
                break
            w *=  0.5 * env.action_space.n
            g += reward
            C[state] += w
            V[state] += w * (g - V[state]) / C[state]

            

    return V

if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)

    value_function = main(args)

    # Print the final value function V
    for row in value_function.reshape(4, 4):
        print(" ".join(["{:5.2f}".format(x) for x in row]))
