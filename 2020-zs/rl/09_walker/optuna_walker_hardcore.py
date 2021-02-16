import optuna
import os

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--n_trials", default=100, type=int)



def optimize(trial):

    # timesteps = trial.suggest_categorical("timesteps", [100000, 300000])
    timesteps = trial.suggest_categorical("timesteps", [250000])

    gamma = trial.suggest_categorical("gamma", [0.98, 0.99])
    frame_skip = trial.suggest_categorical("frame_skip", [1, 2, 3, 4, 5])
    learning_rate = trial.suggest_categorical("learning_rate", [0.003, 0.0015, 0.0007])
    buffer_size = trial.suggest_categorical("buffer_size", [100000,  300000])
    tau = trial.suggest_categorical("tau", [0.01, 0.02])

    batch_size = trial.suggest_categorical("batch_size", [256, 512, 1024])
    train_freq = trial.suggest_categorical("train_freq", [64, 256, 1024])
    gradient_steps = trial.suggest_categorical("gradient_steps", [64])


    cmd = f"python walker.py --batch_size={batch_size} --learning_rate={learning_rate} --gamma={gamma} --timesteps={timesteps} --frame_skip={frame_skip} --buffer_size={buffer_size} --tau={tau} --train_freq={train_freq}  --gradient_steps={gradient_steps}"
    last_line = os.popen(cmd).read().strip().split("\n")[-1]
    print(last_line)
    score = float(last_line.split()[-2])
    print("score:", score)
    return -score



if __name__ == "__main__":
    args = parser.parse_args()

    study = optuna.load_study(study_name='walker-hardcore-distributed', storage='sqlite:///walker_hardcore.db')
    study.optimize(optimize, n_trials=args.n_trials)