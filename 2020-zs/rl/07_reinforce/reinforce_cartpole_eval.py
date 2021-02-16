#!/usr/bin/env python3
import argparse
from RAdam import RAdamOptimizer
import os
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3") # Report only TF errors by default

import gym
import numpy as np
import tensorflow as tf

import wrappers
import cart_pole_pixels_environment

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--recodex", default=True, action="store_true", help="Running in ReCodEx")
parser.add_argument("--render_each", default=0, type=int, help="Render some episodes.")
parser.add_argument("--seed", default=None, type=int, help="Random seed.")
parser.add_argument("--threads", default=8, type=int, help="Maximum number of threads to use.")

# For these and any other arguments you add, ReCodEx will keep your default value.
parser.add_argument("--batch_size", default=6, type=int, help="Batch size.")
parser.add_argument("--episodes", default=20000, type=int, help="Training episodes.")
parser.add_argument("--gamma", default=1, type=float, help="Discounting factor.")
parser.add_argument("--hidden_layer_size", default=28, type=int, help="Size of hidden layer.")
parser.add_argument("--beta", default=0.01, type=float )
parser.add_argument("--hidden_layers", default=2, type=int)
parser.add_argument("--learning_rate", default=0.0003, type=float, help="Learning rate.")
parser.add_argument("--activation", default="relu", type=str)


parser.add_argument("--cnn_filters", default=32, type=float, help="Learning rate.")

parser.add_argument("--grad_clipping", default=0.05, type=float)

parser.add_argument("--dropout", default=0.17, type=float)



def warmup_lr_schedule(episode):
    WARM_PERIOD = 10
    if episode < WARM_PERIOD:
        return args.learning_rate * episode / WARM_PERIOD
    else:
        return args.learning_rate * (0.8**((episode - WARM_PERIOD) * 10 / WARM_PERIOD))



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

        x = tf.keras.layers.Conv2D(filters=args.cnn_filters, kernel_size=8, strides=2 )(inputs)
        x = tf.keras.layers.ReLU()(x)
        # x = tf.keras.layers.Conv2D(filters=args.cnn_filters * 2, kernel_size=4, strides=2)(x)
        # x = tf.keras.layers.ReLU()(x)
        policy_features = tf.keras.layers.Flatten()(x)

        x = tf.keras.layers.Conv2D(filters=args.cnn_filters, kernel_size=8, strides=2)(baseline_inputs)
        x = tf.keras.layers.ReLU()(x)
        # x = tf.keras.layers.Conv2D(filters=args.cnn_filters * 2, kernel_size=4, strides=2)(x)
        # x = tf.keras.layers.ReLU()(x)
        baseline_features = tf.keras.layers.Flatten()(x)

        hidden = policy_features 
        hidden_b = baseline_features 
        for i in range(args.hidden_layers):
            hidden = tf.keras.layers.Dense(args.hidden_layer_size, activation=args.activation, kernel_regularizer='l2')(hidden)
            hidden = tf.keras.layers.Dropout(args.dropout)(hidden)

            hidden_b = tf.keras.layers.Dense(args.hidden_layer_size, activation=args.activation, kernel_regularizer='l2')(hidden_b)
            hidden_b = tf.keras.layers.Dropout(args.dropout)(hidden_b)


        out = tf.keras.layers.Dense(env.action_space.n, activation='softmax')(hidden)
        out_b = tf.keras.layers.Dense(1)(hidden_b)
        out_b = tf.keras.layers.Flatten()(out_b)

        self._model = tf.keras.Model(inputs, out)
        # self._model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(), optimizer=tf.keras.optimizers.Adam(0, clipnorm=args.grad_clipping))
        self._model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(), optimizer=RAdamOptimizer(args.learning_rate ))
        

        self._baseline_model = tf.keras.Model(baseline_inputs, out_b)

        loss = tf.keras.losses.Huber()
        # self._baseline_model.compile(loss=loss, optimizer=tf.keras.optimizers. optimizer=tf.keras.optimizers.Adam(0, clipnorm=args.grad_clipping))
        self._baseline_model.compile(loss=loss, optimizer=RAdamOptimizer(args.learning_rate))



            


    # TODO: Define a training method.
    #
    # Note that we need to use @tf.function for efficiency (using `train_on_batch`
    # on extremely small batches/networks has considerable overhead).
    #
    # The `wrappers.typed_np_function` automatically converts input arguments
    # to NumPy arrays of given type, and converts the result to a NumPy array.
    @wrappers.typed_np_function(np.float32, np.int32, np.float32)
    # @tf.function(experimental_relax_shapes=True)
    def train(self, states, actions, returns):
        # You should:
        # - compute the predicted baseline using the baseline model
        # - train the policy model, using `returns - predicted_baseline` as
        #   advantage estimate
        # - train the baseline model to predict `returns`
        # if the batch-size is too big, split the batch into several splits for memory reasons


        policy_grad = [tf.zeros_like(var)  for var in self._model.trainable_weights]
        baseline_grad = [tf.zeros_like(var)  for var in self._baseline_model.trainable_weights]
 

        split_size = 2000
        for i in range(0, len(states), split_size):
            states_split = states[i:i + split_size]
            actions_split = actions[i:i + split_size]
            returns_split = returns[i:i + split_size]


            with tf.GradientTape() as baseline_tape:
                # shape = (split_size, 1)
                predicted_baseline = self._baseline_model(states_split, training=True)
                # print("pred baseline shape:", predicted_baseline.shape)

                # shape = ()
                baseline_loss = self._baseline_model.loss(returns_split, predicted_baseline) 
                # print("baseline loss shape:", baseline_loss.shape)


            # print("baseline_loss:", baseline_loss)

            with tf.GradientTape() as policy_tape:
                action_pred = self._model(states_split, training=True)

                advantage = returns_split - tf.reshape(predicted_baseline, [-1])
                # advantage = tf.math.l2_normalize(returns_split - tf.reshape(predicted_baseline, [-1]), axis=[-1]) 
                # advantage = tf.map_fn(lambda row: row / tf.math.abs(tf.reduce_sum(row)), advantage)

                policy_loss = self._model.loss(actions_split, action_pred, sample_weight=advantage)

                entropy = - tf.math.reduce_sum(action_pred * tf.math.log(action_pred), axis=-1) / np.log(2)
                policy_loss -= args.beta * entropy



            baseline_grad_split = baseline_tape.gradient(baseline_loss, self._baseline_model.trainable_variables)
            policy_grad_split = policy_tape.gradient(policy_loss, self._model.trainable_variables)

            baseline_grad = [grad + grad_split for grad, grad_split in zip(baseline_grad, baseline_grad_split)]
            policy_grad = [grad + grad_split for grad, grad_split in zip(policy_grad, policy_grad_split)]


            del baseline_grad_split
            del policy_grad_split

        self._model.optimizer.apply_gradients(zip(policy_grad, self._model.trainable_variables))
        self._baseline_model.optimizer.apply_gradients(zip(baseline_grad, self._baseline_model.trainable_variables))

        

    


    # Predict method, again with manual @tf.function for efficiency.
    @wrappers.typed_np_function(np.float32)
    @tf.function
    def predict(self, states):
        return self._model(states)

def main(env, args):
    global network
    # Fix random seeds and number of threads
    np.random.seed(args.seed)
    tf.random.set_seed(args.seed)
    tf.config.threading.set_inter_op_parallelism_threads(args.threads)
    tf.config.threading.set_intra_op_parallelism_threads(args.threads)

    # Construct the network
    network = Network(env, args)

    # Training
    if not args.recodex:
        try: 
            steps = 0
            for ep in range(args.episodes // args.batch_size):
                batch_states, batch_actions, batch_returns = [], [], []
                for _ in range(args.batch_size):
                    # Perform episode
                    states, actions, rewards = [], [], []
                    state, done = env.reset(), False
                    while not done:
                        if args.render_each and env.episode > 0 and env.episode % args.render_each == 0:
                            env.render()

                        dist = network.predict([state])[0]
                        print(dist)
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


                # print("Learning rate:", warmup_lr_schedule(ep))
                # network._baseline_model.optimizer.lr = warmup_lr_schedule(ep)
                # network._model.optimizer.lr = warmup_lr_schedule(ep)

                network.train(batch_states, batch_actions, batch_returns)

                print(steps)
                steps += 1


                network._model.save("checkpoint")

        except KeyboardInterrupt:
            pass
    

    network._model = tf.keras.models.load_model("checkpoint")
        

    print("Evaluation!")

    # Final evaluation
    while True:
        state, done = env.reset(True), False
        while not done:
            action = np.argmax(network.predict([state])[0])
            state, reward, done, _ = env.step(action)


if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)
    env = wrappers.EvaluationWrapper(gym.make("CartPolePixels-v0"), args.seed)
    main(env, args)
