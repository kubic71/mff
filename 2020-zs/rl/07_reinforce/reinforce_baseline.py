#!/usr/bin/env python3
import argparse
import os
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3") # Report only TF errors by default

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
parser.add_argument("--batch_size", default=6, type=int, help="Batch size.")
parser.add_argument("--episodes", default=200, type=int, help="Training episodes.")
parser.add_argument("--gamma", default=0.999, type=float, help="Discounting factor.")
parser.add_argument("--hidden_layer_size", default=28, type=int, help="Size of hidden layer.")
parser.add_argument("--hidden_layers", default=2, type=int)
parser.add_argument("--learning_rate", default=0.016, type=float, help="Learning rate.")

parser.add_argument("--activation", default="tanh", type=str)
parser.add_argument("--dropout", default=0.17, type=float)

class Network:
    def __init__(self, env, args):
        # TODO: Create a suitable model.
        #
        # Apart from the model defined in `reinforce`, define also another
        # model for computing baseline (with one output, using a dense layer
        # without activation).
        #
        # Using Adam optimizer with given `args.learning_rate` for both models
        # is a good default.
        inputs = tf.keras.Input(shape=env.observation_space.shape)
        baseline_inputs = tf.keras.Input(shape=env.observation_space.shape)

        hidden = inputs
        hidden_b = baseline_inputs
        for i in range(args.hidden_layers):
            hidden = tf.keras.layers.Dense(args.hidden_layer_size, activation=args.activation, kernel_regularizer='l2')(hidden)
            hidden = tf.keras.layers.Dropout(args.dropout)(hidden)

            hidden_b = tf.keras.layers.Dense(args.hidden_layer_size, activation=args.activation, kernel_regularizer='l2')(hidden_b)
            hidden_b = tf.keras.layers.Dropout(args.dropout)(hidden_b)


        out = tf.keras.layers.Dense(env.action_space.n, activation='softmax')(hidden)
        out_b = tf.keras.layers.Dense(1)(hidden_b)
        out_b = tf.keras.layers.Flatten()(out_b)

        self._model = tf.keras.Model(inputs, out)
        self._model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(), optimizer=tf.keras.optimizers.Adam(args.learning_rate))

        self._baseline_model = tf.keras.Model(baseline_inputs, out_b)
        self._baseline_model.compile(loss=tf.keras.losses.MeanSquaredError(), optimizer=tf.keras.optimizers.Adam(args.learning_rate))
            


    # TODO: Define a training method.
    #
    # Note that we need to use @tf.function for efficiency (using `train_on_batch`
    # on extremely small batches/networks has considerable overhead).
    #
    # The `wrappers.typed_np_function` automatically converts input arguments
    # to NumPy arrays of given type, and converts the result to a NumPy array.
    @wrappers.typed_np_function(np.float32, np.int32, np.float32)
    @tf.function(experimental_relax_shapes=True)
    def train(self, states, actions, returns):
        # You should:
        # - compute the predicted baseline using the baseline model
        # - train the policy model, using `returns - predicted_baseline` as
        #   advantage estimate
        # - train the baseline model to predict `returns`

        with tf.GradientTape() as baseline_tape:
            predicted_baseline = self._baseline_model(states, training=True)
            baseline_loss = self._baseline_model.loss(returns, predicted_baseline)
        

        with tf.GradientTape() as policy_tape:
            action_pred = self._model(states, training=True)

            advantage = returns - tf.reshape(predicted_baseline, [-1])
            policy_loss = self._model.loss(actions, action_pred, sample_weight=advantage)

        baseline_grad = baseline_tape.gradient(baseline_loss, self._baseline_model.trainable_variables)
        self._baseline_model.optimizer.apply_gradients(zip(baseline_grad, self._baseline_model.trainable_variables))

        policy_grad = policy_tape.gradient(policy_loss, self._model.trainable_variables)
        self._model.optimizer.apply_gradients(zip(policy_grad, self._model.trainable_variables))

    


    # Predict method, again with manual @tf.function for efficiency.
    @wrappers.typed_np_function(np.float32)
    @tf.function
    def predict(self, states):
        return self._model(states)

def main(env, args):
    # Fix random seeds and number of threads
    np.random.seed(args.seed)
    tf.random.set_seed(args.seed)
    tf.config.threading.set_inter_op_parallelism_threads(args.threads)
    tf.config.threading.set_intra_op_parallelism_threads(args.threads)

    # Construct the network
    network = Network(env, args)

    # Training
    for _ in range(args.episodes // args.batch_size):
        batch_states, batch_actions, batch_returns = [], [], []
        for _ in range(args.batch_size):
            # Perform episode
            states, actions, rewards = [], [], []
            state, done = env.reset(), False
            while not done:
                if args.render_each and env.episode > 0 and env.episode % args.render_each == 0:
                    env.render()

                dist = network.predict([state])[0]
                action = np.random.choice(env.action_space.n, p=dist)

                next_state, reward, done, _ = env.step(action)

                states.append(state)
                actions.append(action)
                rewards.append(reward)

                state = next_state

            returns = []
            est = 0
            for rew in reversed(rewards):
                new = args.gamma*est + rew
                returns.append(new)
                est  = new

            returns = reversed(returns)

            batch_states += states
            batch_actions += actions
            batch_returns += returns

        # print(len(batch_states))
        network.train(batch_states, batch_actions, batch_returns)

    # Final evaluation
    while True:
        state, done = env.reset(True), False
        while not done:
            action = np.argmax(network.predict([state])[0])
            state, reward, done, _ = env.step(action)


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)

    # Create the environment
    env = wrappers.EvaluationWrapper(gym.make("CartPole-v1"), args.seed)

    main(env, args)
