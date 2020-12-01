#!/usr/bin/env python3
import argparse
import os
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3") # Report only TF errors by default

from RAdam import RAdamOptimizer
import gym
import numpy as np
import tensorflow as tf

import wrappers

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--recodex", default=False, action="store_true", help="Running in ReCodEx")
parser.add_argument("--render_each", default=0, type=int, help="Render some episodes.")
parser.add_argument("--seed", default=None, type=int, help="Random seed.")
parser.add_argument("--threads", default=8, type=int, help="Maximum number of threads to use.")
# For these and any other arguments you add, ReCodEx will keep your default value.
parser.add_argument("--env", default="CartPole-v1", type=str, help="Environment.")
parser.add_argument("--evaluate_each", default=200, type=int, help="Evaluate each number of batches.")
parser.add_argument("--evaluate_for", default=10, type=int, help="Evaluate the given number of episodes.")
parser.add_argument("--gamma", default=0.99, type=float, help="Discounting factor.")
parser.add_argument("--hidden_layer_size", default=512, type=int, help="Size of hidden layer.")
parser.add_argument("--learning_rate", default=0.0003, type=float, help="Learning rate.")
parser.add_argument("--workers", default=32, type=int, help="Number of parallel workers.")

class Network:
    def __init__(self, env, args):
        policy_in = tf.keras.Input(shape=env.observation_space.shape)
        x = tf.keras.layers.Dense(args.hidden_layer_size, activation='relu')(policy_in)
        policy_out = tf.keras.layers.Dense(env.action_space.n, activation='softmax')(x)

        self.policy = tf.keras.Model(policy_in, policy_out)

        self.policy.compile(
            optimizer=RAdamOptimizer(args.learning_rate),
            loss = tf.keras.losses.SparseCategoricalCrossentropy()
        )

        value_in = tf.keras.Input(shape=env.observation_space.shape)
        x = tf.keras.layers.Dense(args.hidden_layer_size, activation='relu')(value_in)
        value_out = tf.keras.layers.Dense(1)(x)

        self.value = tf.keras.Model(value_in, value_out)

        self.value.compile(
            optimizer=RAdamOptimizer(args.learning_rate),
            loss=tf.keras.losses.MeanSquaredError()
        )

    # The `wrappers.typed_np_function` automatically converts input arguments
    # to NumPy arrays of given type, and converts the result to a NumPy array.
    @wrappers.typed_np_function(np.float32, np.int32, np.float32)
    @tf.function
    def train(self, states, actions, returns):
        with tf.GradientTape() as value_tape:
            predicted_vf = self.value(states, training=True)
            value_loss = self.value.loss(returns, predicted_vf)

        with tf.GradientTape() as policy_tape:
            action_pred = self.policy(states, training=True)
            advantage = returns - tf.reshape(predicted_vf, [-1])
            policy_loss = self.policy.loss(actions, action_pred, sample_weight=advantage)

        value_grads = value_tape.gradient(value_loss, self.value.trainable_variables)
        self.value.optimizer.apply_gradients(zip(value_grads, self.value.trainable_variables))

        policy_grads = policy_tape.gradient(policy_loss, self.policy.trainable_variables)
        self.policy.optimizer.apply_gradients(zip(policy_grads, self.policy.trainable_variables))

    @wrappers.typed_np_function(np.float32)
    @tf.function
    def predict_actions(self, states):
        return self.policy(states)

    @wrappers.typed_np_function(np.float32)
    @tf.function
    def predict_values(self, states):
        return self.value(states)[:, 0]


def main(env, args):
    # Fix random seeds and number of threads
    np.random.seed(args.seed)
    tf.random.set_seed(args.seed)
    tf.config.threading.set_inter_op_parallelism_threads(args.threads)
    tf.config.threading.set_intra_op_parallelism_threads(args.threads)

    # Construct the network
    network = Network(env, args)

    def evaluate_episode(start_evaluation=False):
        rewards, state, done = 0, env.reset(start_evaluation), False
        while not done:
            if args.render_each and env.episode > 0 and env.episode % args.render_each == 0:
                env.render()

            probabilities = network.predict_actions([state])[0]
            action = np.argmax(probabilities)
            state, reward, done, _ = env.step(action)
            rewards += reward
        return rewards

    # Create the vectorized environment
    vector_env = gym.vector.AsyncVectorEnv([lambda: gym.make(env.spec.id)] * args.workers)
    states = vector_env.reset()

    training = True
    while training:
        # Training
        for _ in range(args.evaluate_each):
            probabilities = network.predict_actions(states)
            # print(probabilities)
            actions = np.array([np.random.choice(env.action_space.n, p=action_p) for action_p in probabilities])

            next_states, rewards, dones, _ = vector_env.step(actions)

            predicted_values = network.predict_values(next_states)
            return_estimates = rewards + (args.gamma * np.array([0 if done else pred for done, pred in zip(dones, predicted_values)]))

            network.train(states, actions, return_estimates)
            states = next_states

        for _ in range(args.evaluate_for):
            evaluate_episode()


        if sum(env._episode_returns[-100:])/100 > 400:
            training = False

    # Final evaluation
    while True:
        evaluate_episode(start_evaluation=True)


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)

    # Create the environment
    env = wrappers.EvaluationWrapper(gym.make(args.env), args.seed)

    main(env, args)
