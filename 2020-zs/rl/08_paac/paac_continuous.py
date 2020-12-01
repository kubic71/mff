#!/usr/bin/env python3
import argparse
from RAdam import RAdamOptimizer
import os
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3") # Report only TF errors by default

import gym
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

import wrappers

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--recodex", default=False, action="store_true", help="Running in ReCodEx")
parser.add_argument("--render_each", default=100, type=int, help="Render some episodes.")
parser.add_argument("--seed", default=41, type=int, help="Random seed.")
parser.add_argument("--threads", default=8, type=int, help="Maximum number of threads to use.")
# For these and any other arguments you add, ReCodEx will keep your default value.
parser.add_argument("--entropy_regularization", default=None, type=float, help="Entropy regularization weight.")
parser.add_argument("--evaluate_each", default=300, type=int, help="Evaluate each number of batches.")
parser.add_argument("--evaluate_for", default=10, type=int, help="Evaluate the given number of episodes.")
parser.add_argument("--gamma", default=1, type=float, help="Discounting factor.")
parser.add_argument("--beta", default=0.0, type=float, help="Discounting factor.")
parser.add_argument("--hidden_layer_size", default=64, type=int, help="Size of hidden layer.")
parser.add_argument("--learning_rate", default=0.0005, type=float, help="Learning rate.")
parser.add_argument("--tiles", default=16, type=int, help="Tiles to use.")
parser.add_argument("--workers", default=128, type=int, help="Number of parallel workers.")

class Network:
    def __init__(self, env, args):
        # TODO: Analogously to paac, your model should contain two components:
        # - actor, which predicts distribution over the actions
        # - critic, which predicts the value function
        #
        # The given states are tile encoded, so they are integral indices of
        # tiles intersecting the state. Therefore, you should convert them
        # to dense encoding (one-hot-like, with with `args.tiles` ones).
        # (Or you can even use embeddings for better efficiency.)
        #
        # The actor computes `mus` and `sds`, each of shape [batch_size, actions].
        # Compute each independently using states as input, adding a fully connected
        # layer with `args.hidden_layer_size` units and ReLU activation. Then:
        # - For `mus`, add a fully connected layer with `actions` outputs.
        #   To avoid `mus` moving from the required range, you should apply
        #   properly scaled `tf.tanh` activation.
        # - For `sds`, add a fully connected layer with `actions` outputs
        #   and `tf.nn.softplus` activation.
        #
        # The critic should be a usual one, passing states through one hidden
        # layer with `args.hidden_layer_size` ReLU units and then predicting
        # the value function.
        policy_in = tf.keras.Input(shape=args.tiles)
        x = tf.keras.layers.Embedding(env.observation_space.nvec[-1], args.hidden_layer_size, input_length=args.tiles)(policy_in)
        x = tf.keras.layers.GlobalAveragePooling1D(data_format="channels_last")(x)
        x = tf.keras.layers.Dense(args.hidden_layer_size, activation='relu')(x)

        self.mu = tf.keras.layers.Dense(1, activation=lambda x: tf.constant(2.0) * tf.tanh(x))(x)
        self.sd = tf.keras.layers.Dense(1, activation=tf.keras.activations.softplus)(x)
        policy_out = tf.keras.layers.Concatenate()([self.mu, self.sd])

        self.actor = tf.keras.Model(policy_in, policy_out)
        self.policy_optimizer = RAdamOptimizer(args.learning_rate)

        value_in = tf.keras.Input(shape=args.tiles)
        x = tf.keras.layers.Embedding(env.observation_space.nvec[-1], args.hidden_layer_size, input_length=args.tiles)(value_in)
        x = tf.keras.layers.GlobalAveragePooling1D(data_format="channels_last")(x)
        x = tf.keras.layers.Dense(args.hidden_layer_size, activation='relu')(x)
        value_out = tf.keras.layers.Dense(1)(x)
        self.critic = tf.keras.Model(value_in, value_out)
        self.critic.compile(
            optimizer=RAdamOptimizer(args.learning_rate),
            loss=tf.keras.losses.MeanSquaredError()
        )


    @wrappers.typed_np_function(np.float32, np.float32, np.float32)
    @tf.function
    def train(self, states, actions, returns):

        with tf.GradientTape() as critic_tape:
            pred_values = self.critic(states)
            critic_loss = self.critic.loss(returns, pred_values)

        critic_grads = critic_tape.gradient(critic_loss, self.critic.trainable_variables)
        self.critic.optimizer.apply_gradients(zip(critic_grads, self.critic.trainable_variables))

        with tf.GradientTape() as policy_tape:
            pred_actions = self.actor(states)
            mus = pred_actions[:, 0]
            sds = pred_actions[:, 1]
            
            # mus = tf.clip_by_value(mus, clip_value_min=-1, clip_value_max=1)
            # sds = tf.clip_by_value(sds, clip_value_min=0, clip_value_max=1)
            action_distribution = tfp.distributions.Normal(mus, sds)

            advantage = returns - pred_values[:, 0]
            nll = -action_distribution.log_prob(actions[:, 0])
            loss = nll * advantage
            policy_loss = tf.math.reduce_mean(loss)

            # entropy penalization
            entropy = tf.math.reduce_mean(tf.math.log(sds))
            # policy_loss -= args.beta * entropy

            # print(policy_loss)


        # print("Policy_loss", policy_loss)
        # print(self.actor.trainable_variables)
        policy_grad = policy_tape.gradient(policy_loss, self.actor.trainable_variables)
        # print(policy_grad)
        self.policy_optimizer.apply_gradients(zip(policy_grad, self.actor.trainable_variables))

        # TODO: Run the model on given `states` and compute
        # sds, mus and predicted values. Then create `action_distribution` using
        # `tfp.distributions.Normal` class and computed mus and sds.
        # In PyTorch, the corresponding class is `torch.distributions.normal.Normal`.
        #
        # TODO: Compute total loss as a sum of three losses:
        # - negative log likelihood of the `actions` in the `action_distribution`
        #   (using the `log_prob` method). You then need to sum the log probabilities
        #   of actions in a single batch example (using `tf.math.reduce_sum` with `axis=1`).
        #   Finally multiply the resulting vector by (returns - predicted values)
        #   and compute its mean. Note that the gradient must not flow through
        #   the predicted values (you can use `tf.stop_gradient` if necessary).
        # - negative value of the distribution entropy (use `entropy` method of
        #   the `action_distribution`) weighted by `args.entropy_regularization`.
        # - mean square error of the `returns` and predicted values.

    @wrappers.typed_np_function(np.float32)
    @tf.function
    def predict_actions(self, states):
        # TODO: Return predicted action distributions (mus and sds).
        mus_sds = tf.transpose(self.actor(states), (1, 0))
        # return tf.clip_by_value(mus_sds[0], -1, 1), tf.clip_by_value(mus_sds[1], 0, 1)
        return mus_sds

    @wrappers.typed_np_function(np.float32)
    @tf.function
    def predict_values(self, states):
        # TODO: Return predicted state-action values.
        return self.critic(states)[:, 0]


def main(env, args):
    global vector_env
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

            mus, sds = network.predict_actions([state])
            mu, sd = mus[0], sds[0]
            # action = np.clip(np.random.normal(mu, sd), -1, 1)
            action = np.clip(mu, -1, 1)

            return_estimate = network.predict_values([state])[0]

            # print(f"mu:\t{mu}\tsd:\t{sd}\taction:\t{action}\treturn_est:\t{return_estimate}")
            # mus, _ = network.predict_actions([state])

            state, reward, done, _ = env.step([action])
            rewards += reward
        return rewards

    # Create the vectorized environment
    vector_env = gym.vector.AsyncVectorEnv(
        [lambda: wrappers.DiscreteMountainCarWrapper(gym.make("MountainCarContinuous-v0"), tiles=args.tiles)] * args.workers)
    vector_env.seed(args.seed)
    states = vector_env.reset()

    training = True
    while training:
        # Training
        for _ in range(args.evaluate_each):
            # TODO: Predict action distribution using `network.predict_actions`
            # and then sample it using for example `np.random.normal`. Do not
            # forget to clip the actions to the `env.action_space.{low,high}`
            # range, for example using `np.clip`.
            mus, sds = network.predict_actions(states)
            actions = np.reshape(np.random.normal(mus, sds), (args.workers, 1))
            # print(actions)

            # TODO(paac): Perform steps in the vectorized environment
            next_states, rewards, dones, _ = vector_env.step(np.clip(actions, -1, 1))

            # rewards -= 1

            # TODO(paac): Compute estimates of returns by one-step bootstrapping
            predicted_values = network.predict_values(next_states)
            return_estimates = rewards + (args.gamma * np.array([0 if done else pred for done, pred in zip(dones, predicted_values)]))

            # TODO(paac): Train network using current states, chosen actions and estimated returns
            network.train(states, actions, return_estimates)
            states = next_states


        # Periodic evaluation
        for _ in range(args.evaluate_for):
            evaluate_episode()

        if sum(env._episode_returns[-100:]) / min(100, len(env._episode_returns)) > 90:
            training = False

    # Final evaluation
    while True:
        evaluate_episode(start_evaluation=True)


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)

    # Create the environment
    env = wrappers.EvaluationWrapper(wrappers.DiscreteMountainCarWrapper(gym.make("MountainCarContinuous-v0"), tiles=args.tiles), args.seed)

    main(env, args)
