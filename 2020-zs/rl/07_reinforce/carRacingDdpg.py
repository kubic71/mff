# from stable_baselines3 import DDPG
# from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback, EveryNTimesteps






import argparse
import wrappers
import tensorflow as tf
import numpy as np
import gym
# from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise
import os
import functools


parser = argparse.ArgumentParser()
# These arguments will be set appropriately by ReCodEx, even if you change them.
parser.add_argument("--recodex", default=False,
                    action="store_true", help="Running in ReCodEx")
parser.add_argument("--seed", default=9840, type=int, help="Random seed.")
parser.add_argument("--checkpoint_every", default=5000, type=int)


parser.add_argument("--frame_skip", default=4, type=int, help="Frame skip.")

parser.add_argument("--batch_size", default=2048, type=int)
parser.add_argument("--gamma", default=0.995, type=float)
parser.add_argument("--controller_size", default=64, type=int)
parser.add_argument("--controller_depth", default=2, type=int)

parser.add_argument("--epsilon", default=0.4, type=float)
parser.add_argument("--epsilon_final", default=0.1, type=float)
parser.add_argument("--epsilon_final_at", default=0.5, type=float)


parser.add_argument("--render_every", default=10, type=int)
parser.add_argument("--save_to", default="dqn_racecar", type=str)
parser.add_argument("--load_from", default=None, type=str)
parser.add_argument("--logdir", default="logs", type=str)


parser.add_argument("--discrete_actions", default=True, action="store_false")
parser.add_argument("--total_timesteps", default=1000000, type=int)


parser.add_argument("--action_map", default="small", type=str)

parser.add_argument("--buffer_size", default=1000000, type=int)
parser.add_argument("--train_freq", default=4, type=int)

# Reward shaping
parser.add_argument("--green_penalty", default=200, type=float)
parser.add_argument("--skidding_penalty", default=1, type=float)

parser.add_argument("--speed_limit_penalty", default=0, type=float)
parser.add_argument("--speed_limit_end", default=2, type=float)

# parser.add_argument("--skid_penalty", default=2, type=float)



parser.add_argument("--min_speed", default=1.2, type=float)
parser.add_argument("--min_speed_start", default=0.5, type=float)
parser.add_argument("--min_speed_penalty", default=0.0, type=float)

parser.add_argument("--silent", default=False, action="store_true" )

parser.add_argument("--original_gym", default=False, action="store_true")

# Only for DQN
parser.add_argument("--target_update_interval", default=5000, type=int)
parser.add_argument("--learning_starts", default=3000, type=int)
parser.add_argument("--tau", default=1, type=float)

parser.add_argument("--lr", default=0.0001, type=float)

# Only for DDPG
parser.add_argument("--action_noise", default=0.1, type=float, help="Action noise std.")

# Evaluation
parser.add_argument("--evaluate_for", default=100, type=int) 




def make_env(seed, silent=False):

    def _init():
        if args.original_gym:
            env = gym.make("CarRacing-v0") 
        else:
            env = gym.make("CarRacingSoftFS{}-v0".format(args.frame_skip))

        env = wrappers.VaeCarWrapper(env, silent=silent)
        if not args.recodex:
            env = wrappers.TerminateEarlyWrapper(env)

        if args.discrete_actions:
            env = wrappers.CarDiscretizatinoWrapper(env, args.action_map == "large")

        env = wrappers.EvaluationWrapper(env, args.seed, evaluate_for=args.evaluate_for, render_every=args.render_every,
                                         report_each=1, logname=args.logdir + "/" + get_params_str(seed))

        env = wrappers.RewardWrapper(env, green_penalty=args.green_penalty,
            args=args,
            silent=silent)
        return env

    return _init

def get_params_str(seed):
    if args.discrete_actions:
        return f"DQN,fs={args.frame_skip},lr={args.lr},skid_pen={args.skidding_penalty:.2f},gp={args.green_penalty:.2f},eps={args.epsilon:.2f},eps_fin={args.epsilon_final:.2f},eps_fin_at={args.epsilon_final_at:.2f},l_start={args.learning_starts},train_freq={args.train_freq},target_up_freq={args.target_update_interval},bs={args.batch_size},g={args.gamma:.2f},c_s={args.controller_size},c_d={args.controller_depth},ts={args.total_timesteps},buf_s={args.buffer_size},seed={seed}"
    else:

        # TODO
        return f"DDPG,fs={args.frame_skip},noise={args.action_noise},gp={args.green_penalty},cx_len={args.context_length},bs={args.batch_size},g={args.gamma},c_size={args.controller_size},timesteps={args.total_timesteps},buf_s={args.buffer_size},seed={seed}"


def evaluate(model, seed):
    print("Evaluating!")

    while True:
        state, done = env.reset(start_evaluation=True), False
        while not done:
            env.render()
            # action = np.argmax(model.forward(state))
            action, _states = model.predict(state, deterministic=True)
            state, reward, done, _ = env.step(action)


def load_controller():
    seq = th.nn.Sequential(
            th.nn.Linear(in_features=40, out_features=64, bias=True),
            th.nn.ReLU(),
            th.nn.Linear(in_features=64, out_features=64, bias=True),
            th.nn.ReLU(),
            th.nn.Linear(in_features=64, out_features=5, bias=True)
    )

    sd = seq.state_dict()

    wb = np.load('named_params.npy', allow_pickle=True)

    w0 = wb[0][1].data
    b0 = wb[1][1].data
    w1 = wb[2][1].data
    b1 = wb[3][1].data
    w2 = wb[4][1].data
    b2 = wb[5][1].data

    sd['0.weight'].copy_(w0)
    sd['0.bias'].copy_(b0)
    sd['2.weight'].copy_(w1)
    sd['2.bias'].copy_(b1)
    sd['4.weight'].copy_(w2)
    sd['4.bias'].copy_(b2)

    return seq




if __name__ == "__main__":
    args = parser.parse_args([] if "__file__" not in globals() else None)

    print(get_params_str(args.seed))

    env = make_env(seed=args.seed, silent=args.silent)()

    if args.load_from is not None:
        print("loading model", args.load_from)
        model = DQN.load(args.load_from)
        # model.set_env(env)

        # models = load_controller()

    if not args.recodex and args.total_timesteps > 0:

        policy_kwargs = dict(net_arch=[args.controller_size] * args.controller_depth)


        if args.load_from is None:
            if args.discrete_actions:
                model = DQN('MlpPolicy', env, tau=args.tau, learning_rate=args.lr, exploration_initial_eps=args.epsilon, exploration_final_eps=args.epsilon_final, exploration_fraction=args.epsilon_final_at, train_freq=args.train_freq,
                            batch_size=args.batch_size, buffer_size=args.buffer_size, gamma=args.gamma, target_update_interval=args.target_update_interval, learning_starts=args.learning_starts, policy_kwargs=policy_kwargs, verbose=1)

            else:
                # The noise objects for DDPG
                n_actions = env.action_space.shape[-1]
                # action_noise = NormalActionNoise(mean=np.zeros(
                    # n_actions), sigma=args.action_noise * np.ones(n_actions))

                # model = DDPG('MlpPolicy', env, action_noise=action_noise, batch_size=args.batch_size,
                            #  buffer_size=args.buffer_size, gamma=args.gamma, policy_kwargs=policy_kwargs, verbose=1)

        checkpoint_on_event = CheckpointCallback(save_freq=1, name_prefix=get_params_str(args.seed) , save_path='./checkpoints/')
        event_callback = EveryNTimesteps(n_steps=args.checkpoint_every, callback=checkpoint_on_event)

        model.learn(total_timesteps=args.total_timesteps, log_interval=1, callback=event_callback)

        if(args.save_to):
            model.save(args.save_to)
        else:
            model.save("saved_models/" + get_params_str(f"envSeed-{args.seed}"))

    if args.evaluate_for:
        evaluate(model, env)