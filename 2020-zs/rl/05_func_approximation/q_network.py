#!/usr/bin/env python3
import wrappers
import tensorflow as tf
import numpy as np
import gym
import argparse
import collections
import os
# Report only TF errors by default
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")


parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--recodex", default=False,
                    action="store_true", help="Running in ReCodEx")
parser.add_argument("--render_each", default=0, type=int,
                    help="Render some episodes.")
parser.add_argument("--seed", default=None, type=int, help="Random seed.")
parser.add_argument("--threads", default=16, type=int,
                    help="Maximum number of threads to use.")
# For these and any other arguments you add, ReCodEx will keep your default value.
parser.add_argument("--batch_size", default=128, type=int, help="Batch size.")
parser.add_argument("--epsilon", default=1, type=float,
                    help="Exploration factor.")
parser.add_argument("--epsilon_final", default=0.1,
                    type=float, help="Final exploration factor.")
parser.add_argument("--epsilon_final_at", default=0.4,
                    type=float, help="Training episodes.")
parser.add_argument("--episodes", default=3000,
                    type=int, help="Training episodes.")
parser.add_argument("--gamma", default=0.99, type=float,
                    help="Discounting factor.")
parser.add_argument("--hidden_layer_size", default=24,
                    type=int, help="Size of hidden layer.")
parser.add_argument("--learning_rate", default=0.003,
                    type=float, help="Learning rate.")
parser.add_argument("--target_update_freq", default=200,
                    type=int, help="Target update frequency.")
parser.add_argument("--train_freq", default=100,
                    type=int)
parser.add_argument("--train_threshold", default=430,
                    type=int)

parser.add_argument("--load_from", default="best",
                    type=str)

parser.add_argument("--buffer_size", default=500000, type=int)


def get_log_name():
    return f"epsilon={args.epsilon},epsilon_final={args.epsilon_final},epsilon_final_at={args.epsilon_final_at},episodes={args.episodes},gamma={args.gamma},hidden_size={args.hidden_layer_size},lr={args.learning_rate},target_update_freq={args.target_update_freq},train_freq={args.train_freq},buffer_size={args.buffer_size},batch_size={args.batch_size},seed={args.seed}"


class Network:
    def __init__(self, env, args):
        # TODO: Create a suitable model. The rest of the code assumes
        # it is stored as `self._model` and has been `.compile()`-d.
        inputs = tf.keras.Input(shape=(env.observation_space.shape[0]))
        hidden = tf.keras.layers.Dense(
            args.hidden_layer_size, activation='relu')(inputs)

        outputs = tf.keras.layers.Dense(
            env.action_space.n, activation="relu")(hidden)

        self._model = tf.keras.Model(
            inputs=inputs, outputs=outputs, name="cartpole_model")

        self._model.compile(
            loss=tf.keras.losses.MSE,
            optimizer=tf.keras.optimizers.Adam(args.learning_rate),
            metrics=['accuracy'],
        )

    def save(self, name):
        self._model.save_weights(name)

    def load(self, name):
        self._model.load_weights(name)

    # Define a training method. Generally you have two possibilities
    # - pass new q_values of all actions for a given state; all but one are the same as before
    # - pass only one new q_value for a given state, and include the index of the action to which
    #   the new q_value belongs
    # The code below implements the first option, but you can change it if you want.
    # Also note that we need to use @tf.function for efficiency (using `train_on_batch`
    # on extremely small batches/networks has considerable overhead).
    @tf.function
    def train(self, states, q_values):
        self._model.optimizer.minimize(
            lambda: self._model.loss(
                q_values, self._model(states, training=True)),
            var_list=self._model.trainable_variables
        )

    # Predict method, again with manual @tf.function for efficiency.
    @tf.function
    def predict(self, states):
        return self._model(states)

    # If you want to use target network, the following method copies weights from
    # a given Network to the current one.
    def copy_weights_from(self, other):
        for var, other_var in zip(self._model.variables, other._model.variables):
            var.assign(other_var)


def epsilon_greedy(action, epsilon):
    return np.random.randint(env.action_space.n) if np.random.random() < epsilon else action


def sample_batch(replay_buffer, model, target, bs):
    global states, rewards, actions, next_states, gold, pred, q_values, dones

    states = np.zeros(
        shape=(bs, env.observation_space.shape[0]), dtype=np.float32)
    rewards = np.zeros(shape=(bs,))
    dones = np.zeros(shape=(bs,))
    actions = np.zeros(shape=(bs,), dtype=np.int32)
    next_states = np.zeros(
        shape=(bs, env.observation_space.shape[0]), dtype=np.float32)
    q_values = np.zeros(shape=(bs, env.action_space.n))
    gold = np.zeros(shape=(bs,))

    for i in range(bs):
        sample = replay_buffer[np.random.randint(len(replay_buffer))]
        states[i] = sample.state
        next_states[i] = sample.next_state
        actions[i] = sample.action
        rewards[i] = sample.reward
        dones[i] = sample.done

    pred = target.predict(next_states)
    gold = rewards + args.gamma * np.max(pred, axis=1) * (1 - dones)

    q_values = np.array(model.predict(states))

    for i in range(bs):
        q_values[i, actions[i]] = gold[i]

    return states, q_values


def main(env, args):
    global network, target, replay_buffer, steps
    # Fix random seeds and number of threads
    np.random.seed(args.seed)
    tf.random.set_seed(args.seed)
    tf.config.threading.set_inter_op_parallelism_threads(args.threads)
    tf.config.threading.set_intra_op_parallelism_threads(args.threads)

    # Construct the network
    network = Network(env, args)

    if args.load_from:
        network.load(args.load_from)

    target = Network(env, args)
    target.copy_weights_from(network)

    # Replay memory; maxlen parameter can be passed to deque for a size limit,
    # which we however do not need in this simple task.
    replay_buffer = collections.deque(maxlen=args.buffer_size)
    Transition = collections.namedtuple(
        "Transition", ["state", "action", "reward", "done", "next_state"])

    epsilon = args.epsilon
    training = True

    step = 0
    while env.episode < args.episodes and not args.recodex:

        # Perform episode
        state, done = env.reset(), False

        if env.mean_score(300) > args.train_threshold:
            network.save(f"{env.mean_score(300)}")
            break

        while not done:
            step += 1
            if args.render_each and env.episode > 0 and env.episode % args.render_each == 0:
                env.render()

            # TODO: Choose an action.
            # You can compute the q_values of a given state by
            q_values = network.predict(np.array([state], np.float32))[0]
            action = epsilon_greedy(np.argmax(q_values), epsilon)

            next_state, reward, done, _ = env.step(action)

            # Append state, action, reward, done and next_state to replay_buffer
            replay_buffer.append(Transition(
                state, action, reward, done, next_state))

            # TODO: If the replay_buffer is large enough, preform a training batch
            # from `args.batch_size` uniformly randomly chosen transitions.
            #
            # After you choose `states` and suitable targets, you can train the network as
            #   network.train(states, ...)

            if step % args.train_freq == 0 and len(replay_buffer) >= args.batch_size:
                states, q_values = sample_batch(
                    replay_buffer, network, target, args.batch_size)
                network.train(states, q_values)

            if step % args.target_update_freq == 0:
                target.copy_weights_from(network)

            state = next_state

        if args.epsilon_final_at:
            epsilon = np.interp(
                env.episode + 1, [0, args.epsilon_final_at * args.episodes], [args.epsilon, args.epsilon_final])

    # Final evaluation
    while True:
        state, done = env.reset(start_evaluation=True), False
        while not done:
            if args.render_each == 1:
                env.render()    
            action = np.argmax(network.predict(
                np.array([state], np.float32))[0])
            state, reward, done, _ = env.step(action)



if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)

    # Create the environment
    env = wrappers.EvaluationWrapper(
        gym.make("CartPole-v1"), args.seed, logname="logs/" + get_log_name())

    main(env, args)
