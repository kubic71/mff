

import wrappers
import torch as th
import numpy as np
import gym
import optuna

# from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise
import os


import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--timesteps", default=200000, type=int)
parser.add_argument("--n_trials", default=30, type=int)
parser.add_argument("--evaluate_for", default=50, type=int)


def make_env(silent=False):

    def _init():

        env = gym.make("CarRacingSoftFS{}-v0".format(1))

        env = wrappers.VaeCarWrapper(env, silent=silent)
        env = wrappers.TerminateEarlyWrapper(env)
        env = wrappers.CarDiscretizatinoWrapper(env)
        env = wrappers.EvaluationWrapper(env, np.random.randint(0, 100000), evaluate_for=1,
                                         report_each=1, logname="/dev/null")
        return env

    return _init

def evaluate(trial):

     # Uniform parameter
    fs = trial.suggest_int('frame_skip', 3, 3)
    lr = trial.suggest_loguniform('learning_rate', 1e-5, 1e-3)
    gamma = trial.suggest_categorical("gamma", [0.99])
    epsilon = trial.suggest_uniform("epsilon", 0.3, 1)
    eps_final = trial.suggest_uniform("epsilon_final", 0.05, 0.2)
    eps_final_at = trial.suggest_uniform("epsilon_final_at", 0.2, 1)
    
    cs = trial.suggest_int("controller_size", 32, 128)
    cd = trial.suggest_int("controller_depth", 1, 4)

    green_penalty = trial.suggest_loguniform("green_penalty", 1, 200)
    skidding_penalty = trial.suggest_loguniform("skidding_penalty", 0.5, 20)
    target_update_interval = int(trial.suggest_loguniform("update_interval", 100, 5000))
    
    trial_name = f"optuna/frame_skip={fs},gamma={gamma:.2f},controller_size={cs},controller_depth={cd},epsilon={epsilon:.2f},epsilon_final={eps_final:.2f},epsilon_final_at={eps_final_at:.2f},green_penalty={green_penalty:.2f},skidding_penalty={skidding_penalty:.2f},target_update_interval={target_update_interval}"
    output = os.popen(f"python carRacingDdpg.py --silent --frame_skip={fs} --render_every=0 --gamma={gamma} --total_timesteps={args.timesteps} --controller_size={cs} --controller_depth={cd} --epsilon={epsilon} --epsilon_final={eps_final} --epsilon_final_at={eps_final_at} --green_penalty={green_penalty} --skidding_penalty={skidding_penalty} --target_update_interval={target_update_interval} --evaluate_for=0 --save_to={trial_name} 2>&1  > /dev/null &&  python evaluate_model.py --load_from={trial_name} --evaluate_for={args.evaluate_for} 2> /dev/null | tail -n1").read().strip().split()
#    print(output)
    return -float(output[-2])



if __name__ == "__main__":

    args = parser.parse_args()

    study = optuna.create_study()
    study.optimize(evaluate, n_trials=args.n_trials)