#!/usr/bin/env python3
import argparse

import numpy as np

class GridWorld:
    # States in the gridworld are the following:
    # 0 1 2 3
    # 4 x 5 6
    # 7 8 9 10

    # The rewards are +1 in state 10 and -100 in state 6

    # Actions are ↑ → ↓ ←; with probability 80% they are performed as requested,
    # with 10% move 90° CCW is performed, with 10% move 90° CW is performed.
    states = 11

    actions = ["↑", "→", "↓", "←"]

    @staticmethod
    def step(state, action):
        return [GridWorld._step(0.8, state, action),
                GridWorld._step(0.1, state, (action + 1) % 4),
                GridWorld._step(0.1, state, (action + 3) % 4)]

    @staticmethod
    def _step(probability, state, action):
        if state >= 5: state += 1
        x, y = state % 4, state // 4
        offset_x = -1 if action == 3 else action == 1
        offset_y = -1 if action == 0 else action == 2
        new_x, new_y = x + offset_x, y + offset_y
        if not(new_x >= 4 or new_x < 0  or new_y >= 3 or new_y < 0 or (new_x == 1 and new_y == 1)):
            state = new_x + 4 * new_y
        if state >= 5: state -= 1
        return [probability, +1 if state == 10 else -100 if state == 6 else 0, state]

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--gamma", default=1.0, type=float, help="Discount factor.")
parser.add_argument("--recodex", default=False, action="store_true", help="Running in ReCodEx")
parser.add_argument("--steps", default=1, type=int, help="Number of policy evaluation/improvements to perform.")
# If you add more arguments, ReCodEx will keep them with your default values.

def main(args):

    # 1 backup of bellman operator
    def q(state, action, v, gamma):
        expected_return = 0

        for prob, reward, new_state in GridWorld.step(state, action):
            expected_return += prob * (reward + gamma * v[new_state])

        return expected_return


    def print_lin_eq(vars, const):
        for i, eq in enumerate(vars):
            for j, var in enumerate(eq):
                print("{:>12}".format(f"{var}v[{j}]"), end="")

            print(f"= {const[i]}")



    # Given greedy policy pi, we have system of linear equations for v:
    #
    # v = R + gamma * P_pi * v
    # 
    # or equivalently
    #
    # (I - gamma * P_pi) v = R
    # 
    # where:
    # I is the identity matrix
    # P_pi is the probability transistion matrix, where P_pi[i, j] is the probability of transitioning from state i to state j following policy pi
    # R is the expected reward vector, R[i] is the expected immediate reward from state i following policy pi
    # 
    def solve_v(policy, gamma):
        P_pi = np.zeros(shape=(GridWorld.states, GridWorld.states))
        R = np.zeros(shape=(GridWorld.states,))

        for s in range(GridWorld.states):
            expected_reward = 0

            for prob, reward, new_state in GridWorld.step(s, policy[s]):
                P_pi[s, new_state] += prob
                expected_reward  += prob * reward
            
            R[s] = expected_reward

        A = np.identity(GridWorld.states) - gamma * P_pi

        return np.linalg.solve(A, R)
             

    # Start with zero value function and "go North" policy
    value_function = [0] * GridWorld.states
    policy = [0] * GridWorld.states

    # TODO: Implement policy iteration algorithm, with `args.steps` steps of
    # policy evaluation/policy improvement. During policy evaluation, compute
    # the value function exactly by solving the system of linear equations.
    # During the policy improvement, if multiple actions have the same estimate,
    # choose the one with the smaller index.
    for step in range(args.steps):

        # evaluate policy exactly
        value_function = solve_v(policy, args.gamma)
        
        # update our policy
        for state in range(GridWorld.states):
            policy[state] = np.argmax([q(state, action, value_function, args.gamma) for action in range(len(GridWorld.actions))])

    return value_function, policy

if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    value_function, policy = main(args)

    # Print results
    for l in range(3):
        for c in range(4):
            state = l * 4 + c
            if state >= 5: state -= 1
            print("        " if l == 1 and c == 1 else "{:-8.2f}".format(value_function[state]), end="")
            print(" " if l == 1 and c == 1 else GridWorld.actions[policy[state]], end="")
        print()
