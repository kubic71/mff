#!/usr/bin/env python3
import argparse

import gym
import numpy as np

import wrappers

parser = argparse.ArgumentParser()
parser.add_argument("--episodes", default=2000, type=int, help="Training episodes.")
parser.add_argument("--epsilon", default=0.3, type=float, help="Exploration factor.")
parser.add_argument("--recodex", default=False, action="store_true", help="Running in ReCodEx")
parser.add_argument("--render_each", default=200, type=int, help="Render some episodes.")
parser.add_argument("--seed", default=42, type=int, help="Random seed.")
parser.add_argument("--boxes", default=8, type=int, help="Size of the discretized state space")

def main(env, args):
    # Fix random seed
    np.random.seed(args.seed)

    # TODO:
    # - Create Q, a zero-filled NumPy array with shape [number of states, number of actions],
    #   representing estimated Q value of a given (state, action) pair.
    # - Create C, a zero-filled NumPy array with the same shape,
    #   representing number of observed returns of a given (state, action) pair.
    q = np.zeros((env.observation_space.n, env.action_space.n))
    c = np.zeros((env.observation_space.n, env.action_space.n))

    for episode in range(args.episodes):
        # TODO: Perform episode, collecting states, actions and rewards
        state, done = env.reset(), False
        
        episode_log = []
        
        while not done:
            if args.render_each and env.episode > 0 and env.episode % args.render_each == 0:
                env.render()

            if np.random.random() > args.epsilon * (1 - episode / args.episodes):
            # if np.random.random() > args.epsilon:
                # greedy
                action = np.argmax(q[state])
            else:
                action = np.random.randint(env.action_space.n)

            next_state, reward, done, _ = env.step(action)
            episode_log.append((state, action, reward))
            
            state = next_state

        # TODO: Compute returns from the recieved rewards
        # and update Q and C.
        g = 0
        for state, action, reward in reversed(episode_log):
            g += reward
            c[state, action] = c[state, action] + 1
            q[state, action] = q[state, action] + (g - q[state, action])/c[state, action]


    # Final evaluation
    while True:
        state, done = env.reset(start_evaluation=True), False
        while not done:
            action = np.argmax(q[state])
            state, reward, done, _ = env.step(action)


if __name__ == "__main__":
    args = parser.parse_args()

    # Create the environment
    env = wrappers.EvaluationWrapper(wrappers.DiscreteCartPoleWrapper(gym.make("CartPole-v1"), bins=args.boxes), seed=args.seed, args=args)

    main(env, args)
