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
parser.add_argument("--iterations", default=1, type=int, help="Number of iterations in policy evaluation step.")
parser.add_argument("--recodex", default=False, action="store_true", help="Running in ReCodEx")
parser.add_argument("--steps", default=10, type=int, help="Number of policy evaluation/improvements to perform.")
# If you add more arguments, ReCodEx will keep them with your default values.



def main(args):

    # 1 backup of bellman operator
    def q(state, action, v, gamma):
        expected_return = 0

        for prob, reward, new_state in GridWorld.step(state, action):
            expected_return += prob * (reward + gamma * v[new_state])

        return expected_return


    # Start with zero value function and "go North" policy
    value_function = [0] * GridWorld.states
    policy = [0] * GridWorld.states

    # TODO: Implement policy iteration algorithm, with `args.steps` steps of
    # policy evaluation/policy improvement. During policy evaluation, use the
    # current value function and perform `args.iterations` applications of the
    # Bellman equation. Perform the policy evaluation synchronously (i.e., do
    # not overwrite the current value function when computing its improvement).
    # During the policy improvement, if multiple actions have the same estimate,
    # choose the one with the smaller index.
    for step in range(args.steps):

        # update our value_function estimate
        for it in range(args.iterations):
            new_v = [0] * GridWorld.states

            for state in range(GridWorld.states):
                new_v[state] = q(state, policy[state], value_function, args.gamma)

            value_function = new_v

        # update our policy
        for state in range(GridWorld.states):
            policy[state] = np.argmax([q(state, action, value_function, args.gamma) for action in range(len(GridWorld.actions))])

    # TODO: The final value function should be in `value_function` and final greedy policy in `policy`.
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
