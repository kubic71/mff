from stable_baselines3 import DDPG
from stable_baselines3 import DQN
import argparse
import wrappers
import tensorflow as tf
import numpy as np
import gym
from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise
import os


parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--recodex", default=False,
                    action="store_true", help="Running in ReCodEx")
parser.add_argument("--render_each", default=0, type=int,
                    help="Render some episodes.")
parser.add_argument("--seed", default=None, type=int, help="Random seed.")

parser.add_argument("--frame_skip", default=3, type=int, help="Frame skip.")

parser.add_argument("--batch_size", default=128, type=int)
parser.add_argument("--gamma", default=0.99, type=float)
parser.add_argument("--controller_size", default=64, type=int)
parser.add_argument("--controller_depth", default=2, type=int)

parser.add_argument("--epsilon", default=1, type=float)
parser.add_argument("--epsilon_final", default=0.05, type=float)
parser.add_argument("--epsilon_final_at", default=0.3, type=float)

parser.add_argument("--render_every", default=0, type=int)
parser.add_argument("--save_to", default="dqn_racecar", type=str)
parser.add_argument("--logdir", default="logs", type=str)


parser.add_argument("--discrete_actions", default=False, action="store_true")
parser.add_argument("--total_timesteps", default=5000, type=int)
parser.add_argument("--context_length", default=4, type=int)

parser.add_argument("--buffer_size", default=1000000, type=int)
parser.add_argument("--train_freq", default=50, type=int)

# Reward shaping
parser.add_argument("--green_penalty", default=0.05, type=float)


parser.add_argument("--original_gym", default=False, action="store_true")

# Only for DQN
parser.add_argument("--target_update_interval", default=3000, type=int)
parser.add_argument("--learning_starts", default=3000, type=int)
parser.add_argument("--tau", default=1, type=float)


# Only for DDPG
parser.add_argument("--action_noise", default=0.1, type=float, help="Action noise std.")


# TODO
# - green penalty
# - concatenate multiple frames for context
# - vectorized env?
# - discretize the env
# - expert trajectories
# - punish inactivity
# - skip first 50-or-so frames


args = parser.parse_args([] if "__file__" not in globals() else None)


def get_params_str():
    if args.discrete_actions:
        return f"DQN,fs={args.frame_skip},gp={args.green_penalty},cx_len={args.context_length},tau={args.tau},eps={args.epsilon},eps_fin={args.epsilon_final},eps_fin_at={args.epsilon_final_at},learning_starts={args.learning_starts},train_freq={args.train_freq},target_up_freq={args.target_update_interval},bs={args.batch_size},g={args.gamma},c_size={args.controller_size},c_depth={args.controller_depth},timesteps={args.total_timesteps},buf_size={args.buffer_size},seed={args.seed}"
    else:

        # TODO
        return f"DDPG,fs={args.frame_skip},noise={args.action_noise},gp={args.green_penalty},cx_len={args.context_length},bs={args.batch_size},g={args.gamma},c_size={args.controller_size},timesteps={args.total_timesteps},buf_s={args.buffer_size},seed={args.seed}"


print(get_params_str)

# env.action_space.low = np.array([-1, -1, -1])
# env.action_space.high = np.array([1, 1, 1])

# the noise objects for DDPG



if args.original_gym:
    env = gym.make("CarRacing-v0") 
else:
    env = gym.make("CarRacingSoftFS{}-v0".format(args.frame_skip))

env = wrappers.TerminateEarlyWrapper(wrappers.VaeCarWrapper(env, context_size=args.context_length))

policy_kwargs = dict(net_arch=[args.controller_size] * args.controller_depth)

if args.discrete_actions:
    env = wrappers.CarDiscretizatinoWrapper(env)

env = wrappers.EvaluationWrapper(env, args.seed, evaluate_for=50, render_every=args.render_every,
                                 report_each=1, logname=args.logdir + "/" + get_params_str())

env = wrappers.RewardWrapper(env, green_penalty=args.green_penalty)


if args.discrete_actions:
    model = DQN('MlpPolicy', env, tau=args.tau, exploration_initial_eps=args.epsilon, exploration_final_eps=args.epsilon_final, exploration_fraction=args.epsilon_final_at, train_freq=args.train_freq,
                batch_size=args.batch_size, buffer_size=args.buffer_size, gamma=args.gamma, target_update_interval=args.target_update_interval, learning_starts=args.learning_starts, policy_kwargs=policy_kwargs, verbose=1)

else:
    # The noise objects for DDPG
    n_actions = env.action_space.shape[-1]
    action_noise = NormalActionNoise(mean=np.zeros(
        n_actions), sigma=args.action_noise * np.ones(n_actions))

    model = DDPG('MlpPolicy', env, action_noise=action_noise, batch_size=args.batch_size,
                 buffer_size=args.buffer_size, gamma=args.gamma, policy_kwargs=policy_kwargs, verbose=1)

print(model.policy.parameters_to_vector())
model.learn(total_timesteps=args.total_timesteps, log_interval=10)


if args.total_timesteps > 0:
    model.save("saved_models/" + get_params_str())

# env = model.get_env()

del model  # remove to demonstrate saving and loading

model = DQN.load(
    "saved_models/" + get_params_str()) if args.discrete_actions else DDPG.load(args.save_to)

print("Evaluating!")
while True:
    state, done = env.reset(start_evaluation=True), False
    while not done:
        env.render()
        action, _states = model.predict(state)
        print("action-shape:", action.shape)
        print("action:", action)
        # TODO: Choose an action
        state, reward, done, _ = env.step(action)

