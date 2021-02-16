#!/usr/bin/env python3
import argparse

# from baselines import DQN
from PIL import Image

from torch import nn
import torch as th
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor

from stable_baselines333 import PPO, HER, A2C
import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3") # Report only TF errors by default

import gym
import numpy as np
import tensorflow as tf

import cart_pole_pixels_environment
import wrappers

parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--recodex", default=False, action="store_true", help="Running in ReCodEx")
parser.add_argument("--render_each", default=0, type=int, help="Render some episodes.")
parser.add_argument("--seed", default=None, type=int, help="Random seed.")
parser.add_argument("--threads", default=8, type=int, help="Maximum number of threads to use.")

parser.add_argument("--batch_size", default=32, type=int)
parser.add_argument("--gamma", default=0.99, type=float)

parser.add_argument("--epsilon", default=0.5, type=float)
parser.add_argument("--epsilon_final", default=0.1, type=float)
parser.add_argument("--epsilon_final_at", default=0.5, type=float)

parser.add_argument("--buffer_size", default=100000, type=int)
parser.add_argument("--train_freq", default=4, type=int)

parser.add_argument("--target_update_interval", default=5000, type=int)
parser.add_argument("--learning_starts", default=10000, type=int)
parser.add_argument("--lr", default=0.0001, type=float)

parser.add_argument("--max_grad_norm", default=10, type=float)
parser.add_argument("--downsample", default=1, type=float)

# CNN params
parser.add_argument("--cnn_features_dim", default=32, type=int)
parser.add_argument("--n_hidden", default=1, type=int)
parser.add_argument("--dropout_rate", default=0, type=float)

parser.add_argument("--ppo", default=False, action="store_true")
parser.add_argument("--her", default=False, action="store_true")
parser.add_argument("--a2c", default=False, action="store_true")

parser.add_argument("--total_timesteps", default=50000, type=int)

class ImageSpaceConverterWrapper(gym.ObservationWrapper):
    """ Converts Box(0.0, 1.0, (80, 80, 3)) observation space to Box(0, 255, (80, 80, 3), dtype=uint8) """
    def __init__(self, env, downsample = 1, unsymetricity=0.5):
        super().__init__(env)

        self.width = int(80 * downsample)
        self.height = int(self.width * unsymetricity)
    
        self.observation_space = gym.spaces.Box(
            0, 255, shape=(self.height, self.width, 3), dtype=np.uint8)


    def observation(self, frame):
        img = (frame * 255).astype(np.uint8)
        obs = Image.fromarray(img, mode="RGB").resize((self.width, self.height))
        # obs.show()
        # input()
        
        

        return np.array(obs)


class CustomCNN(BaseFeaturesExtractor):
    """
    # :param observation_space: (gym.Space)
    # :param features_dim: (int) Number of features extracted.
        # This corresponds to the number of unit for the last layer.
    """

    def __init__(self, observation_space: gym.spaces.Box, features_dim: int = 256, n_hidden = 1, dropout_rate=0):
        super(CustomCNN, self).__init__(observation_space, features_dim)
        # We assume CxHxW images (channels first)
        # Re-ordering will be done by pre-preprocessing or wrapper
        n_input_channels = observation_space.shape[0]
        # print("n_input_channels:", n_input_channels)
        self.cnn = nn.Sequential(
            nn.Conv2d(n_input_channels, 32, kernel_size=8, stride=4, padding=0),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2, padding=0),
            nn.ReLU(),
            nn.Flatten(),
        )

        # Compute shape by doing one forward pass
        # print(observation_space.shape)
        with th.no_grad():
            n_flatten = self.cnn(
                th.as_tensor(observation_space.sample()[None]).float()
            ).shape[1]


        layers = [nn.Linear(n_flatten, features_dim), nn.ReLU(), nn.Dropout(dropout_rate)]

        for i in range(n_hidden - 1):
            layers.append(nn.Linear(features_dim, features_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))

        self.linear = nn.Sequential(*layers)

    def forward(self, observations: th.Tensor) -> th.Tensor:
        return self.linear(self.cnn(observations))


def main(env, args):
    global model
    # Fix random seeds and number of threads
    np.random.seed(args.seed)
    tf.random.set_seed(args.seed)
    tf.config.threading.set_inter_op_parallelism_threads(args.threads)
    tf.config.threading.set_intra_op_parallelism_threads(args.threads)

    # policy_kwargs = dict(
        # features_extractor_class=CustomCNN,
        # features_extractor_kwargs=dict(features_dim=args.cnn_features_dim, n_hidden = args.n_hidden, dropout_rate=args.dropout_rate),
    # )
    if not args.recodex:

        env = ImageSpaceConverterWrapper(env, args.downsample)

        if args.ppo:
            print("ppo")
            model = PPO("CnnPolicy",  env, max_grad_norm=args.max_grad_norm, policy_kwargs= policy_kwargs)
        elif args.her:
            goal_selection_strategy = 'future'
            model = HER('CnnPolicy', env, DQN, policy_kwargs = policy_kwargs, n_sampled_goal=4, goal_selection_strategy=goal_selection_strategy,
                                                verbose=1)

        elif args.a2c:
            model = ACER("CnnPolicy",  env, max_grad_norm=args.max_grad_norm )
        else:
            model = DQN("CnnPolicy", env, policy_kwargs = policy_kwargs, learning_rate=args.lr, exploration_initial_eps=args.epsilon, exploration_final_eps=args.epsilon_final, exploration_fraction=args.epsilon_final_at, train_freq=args.train_freq,

                            batch_size=args.batch_size, buffer_size=args.buffer_size, gamma=args.gamma, target_update_interval=args.target_update_interval, learning_starts=args.learning_starts, max_grad_norm = args.max_grad_norm, verbose=1)

        model.learn(total_timesteps=args.total_timesteps, log_interval=50)

    print("Evaluation!")
    while True:
        state, done = env.reset(start_evaluation=True), False
        while not done:
            action, _states = model.predict(state, deterministic=True)
            state, reward, done, _ = env.step(action)

if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)

    # Create the environment
    env = wrappers.EvaluationWrapper(gym.make("CartPolePixels-v0"), args.seed)

    main(env, args)
